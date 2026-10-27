import json
import os
import shutil

from lxml import etree

OUTPUT_DIR = "tei_lists"
TEI_NS = "http://www.tei-c.org/ns/1.0"
XML_NS = "http://www.w3.org/XML/1998/namespace"

with open("json_dumps/persons.json", "r", encoding="utf-8") as json_file:
    data = json.load(json_file)

persons = data.values()

nsmap = {None: TEI_NS}

root = etree.Element(f"{{{TEI_NS}}}TEI", nsmap=nsmap)
root.set(f"{{{XML_NS}}}lang", "de")

tei_header = etree.SubElement(root, f"{{{TEI_NS}}}teiHeader")

tei_filedesc = etree.SubElement(tei_header, f"{{{TEI_NS}}}fileDesc")

tei_titlestmt = etree.SubElement(tei_filedesc, f"{{{TEI_NS}}}titleStmt")
tei_title = etree.SubElement(tei_titlestmt, f"{{{TEI_NS}}}title")
tei_title.text = "Personenregister zum Projekt „Die Protokolle des österreichischen Kabinettsrates 1919–1920“"

tei_pubstmt = etree.SubElement(tei_filedesc, f"{{{TEI_NS}}}publicationStmt")
tei_publisher = etree.SubElement(tei_pubstmt, f"{{{TEI_NS}}}publisher", key="https://d-nb.info/gnd/1001454-8")
tei_publisher.text = "Österreichische Akademie der Wissenschaften"

tei_sourcedesc = etree.SubElement(tei_filedesc, f"{{{TEI_NS}}}sourceDesc")
tei_sourcedesc_p = etree.SubElement(tei_sourcedesc, f"{{{TEI_NS}}}p")
tei_sourcedesc_p.text = "Converted from Baserow data dumped as JSON to https://github.com/krp-project/krp-baserow-dump"

tei_text = etree.SubElement(root, f"{{{TEI_NS}}}text")

tei_body = etree.SubElement(tei_text, f"{{{TEI_NS}}}body")

tei_listperson = etree.SubElement(tei_body, f"{{{TEI_NS}}}listPerson")

for person in persons:

    tei_person = etree.SubElement(tei_listperson, f"{{{TEI_NS}}}person", attrib={f"{{{XML_NS}}}id": person["krp_person_id"]})
    tei_persname = etree.SubElement(tei_person, f"{{{TEI_NS}}}persName")
    tei_persname.text = person["label"]

    if person["date_of_birth"] or person["place_of_birth"] or person["Geburtsort"]:
        tei_birth = etree.SubElement(tei_person, f"{{{TEI_NS}}}birth")
        if person["date_of_birth"]:
            tei_birth_date = etree.SubElement(tei_birth, f"{{{TEI_NS}}}date")
            tei_birth_date.set("when-iso", person["date_of_birth"])
            tei_birth_date.text = person["date_of_birth"]
        if person["place_of_birth"] or person["Geburtsort"]:    
            tei_birth_place = etree.SubElement(tei_birth, f"{{{TEI_NS}}}placeName")
            if person["place_of_birth"]:
                tei_birth_place.set("ref", f"#krp_place_id__{person["place_of_birth"][0]["id"]}")
                tei_birth_place.text = person["place_of_birth"][0]["value"]
            elif person["Geburtsort"]:
                tei_birth_place.text = person["Geburtsort"]

    if person["date_of_death"] or person["place_of_death"] or person["Sterbeort"]:
        tei_death = etree.SubElement(tei_person, f"{{{TEI_NS}}}death")
        if person["date_of_death"]:
            tei_death_date = etree.SubElement(tei_death, f"{{{TEI_NS}}}date")
            tei_death_date.set("when-iso", person["date_of_death"])
            tei_death_date.text = person["date_of_death"]
        if person["place_of_death"] or person["Sterbeort"]:    
            tei_death_place = etree.SubElement(tei_death, f"{{{TEI_NS}}}placeName")
            if person["place_of_death"]:
                tei_death_place.set("ref", f"#krp_place_id__{person["place_of_death"][0]["id"]}")
                tei_death_place.text = person["place_of_death"][0]["value"]
            elif person["Sterbeort"]:
                tei_death_place.text = person["Sterbeort"]

    if person["gnd_url"]:
        tei_person_idno = etree.SubElement(tei_person, f"{{{TEI_NS}}}idno", type="URL", subtype="GND")
    
        tei_person_idno.text = person["gnd_url"]


shutil.rmtree(OUTPUT_DIR, ignore_errors=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

file_path = os.path.join(OUTPUT_DIR, 'listperson.xml')

pi = etree.ProcessingInstruction("xml-model","href='http://www.tei-c.org/release/xml/tei/custom/schema/relaxng/tei_all.rng' type='application/xml' schematypens='http://relaxng.org/ns/structure/1.0'")
root.addprevious(pi)

tree = etree.ElementTree(root)

tree.write(file_path, encoding="utf-8", xml_declaration=True, pretty_print=True)