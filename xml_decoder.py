import sys
from base64 import b64decode
from html import unescape
import lxml.etree as ET
import re
import xml.dom.minidom as minidom

character_codification = 'raw_unicode_escape'

repl_type_table = {
    'EmployeeMasterDataBundleReplicationRequest': 'legacy-hci',
    'EmployeeMasterDataReplicationRequest': 'legacy-boomi',
    'EmployeeMasterDataAndOrgAssignmentBundleReplicationRequest': 'bib',
    'EmployeeMasterDataReplicationBundleRequest': 'ptp'
}


def create_xml_tree(xml_string):
    return ET.fromstring(remove_xml_declaration(xml_string))


def remove_xml_declaration(xml_string):
    return re.sub('<\?.*?\?>(\n)?', '', xml_string)


def get_replication_type(ws_name):
    ws_name = re.sub('{.*}', '', ws_name)
    return repl_type_table[ws_name]


def base64decode(string):
    # extra == is to ensure padding -> no padding will decode alright
    return b64decode(string + '==').decode(character_codification)


def html_deentitize(string):
    return unescape(string)


def extract_and_decode(xml, tag_name, decode_function):
    coded_structures = xml.findall('.//{*}'+tag_name)
    decoded_xml = ET.Element('DecodedEmployees')
    for coded_structure in coded_structures:
        xml_string = decode_function(coded_structure.text)
        decoded_xml.append(create_xml_tree(xml_string))

    return decoded_xml


# given a string that is a valid xml, transforms it into a compacted xml notation, removing whitespaces.
def compress_xml(xml):
    if type(xml) is str:
        return re.sub(">[\n\t\s]*<", '><', xml)
    elif type(xml) is ET._Element:
        return ET.fromstring(compress_xml(xml_to_string(xml)))
        # todo: maybe a recursion removing text and tail if text and tail matches '>[\n\t\s]*<', but has children
    else:
        raise TypeError


# xml_to_string :: Element -> String | context: lxml.etree.Element
# transforms XML Object to string format
def xml_to_string(extracted_xml):
    return ET.tostring(extracted_xml, method='html').decode(character_codification)


# given a string that is a valid xml, it indents it
# returns a string if it receives a string
# if it receives an ET._Element, it converts it to a string and calls itself back
def indent_xml(xml):
    if type(xml) is str:
        return minidom.parseString(compress_xml(xml)).toprettyxml()
    if type(xml) is ET._Element:
        return ET.fromstring(indent_xml(xml_to_string(xml)))
    else:
        raise TypeError


def main():

    content = sys.stdin.read()
    # with open('test/payload_filename', 'r') as file:
    #     content = file.read()
    xml_tree = create_xml_tree(content)
    replication_type = get_replication_type(xml_tree.tag)

    # ptp has trasmission with smaller case t for some reason... therefore I am using this method which
    # I think is more elegant, however, it probably is a little less efficient
    ftsd = [x.text for x in xml_tree.findall('.//') if 'fulltransmissionstartdate' in x.tag.lower()]
    ftsd = ftsd[0] if ftsd != [] else "N/A"

    tag_name, decoding_function = None, lambda x: x
    if len(sys.argv) > 1:
        force_arg = sys.argv[1]
        if force_arg == 'base64':
            tag_name, decoding_function = 'SourceSystemOutputBase64', base64decode
        elif force_arg == 'deentitize':
            tag_name, decoding_function = 'SourceSystemOutput', html_deentitize
        else:
            print('Invalid argument "' + force_arg + '"')
            raise Exception()

    else:
        if replication_type == 'legacy-boomi' or replication_type == 'legacy-hci':
            tag_name, decoding_function = 'SourceSystemOutput', html_deentitize
        elif replication_type == 'bib' or replication_type == 'ptp':
            tag_name, decoding_function = 'SourceSystemOutputBase64', base64decode
        else:
            raise Exception()

    decoded = extract_and_decode(xml_tree, tag_name, decoding_function)
    extra_str = '<!-- ' + 'ReplicationType: ' + replication_type + ' | FullTrasmissionStartDate: ' + ftsd + ' -->\n'
    main_str = remove_xml_declaration(indent_xml(ET.tostring(decoded).decode(character_codification)))
    sys.stdout.write(extra_str+main_str)


if __name__ == "__main__":
    main()


