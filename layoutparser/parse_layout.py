#!/usr/bin/python
from lxml import etree
import sys

#definitions
namespace = "http://schemas.android.com/apk/res/android"
divider = "\n" + ("-"*80) +"\n\n"

#setup lists for each section
variableDefinition = []
onCreate = []
onClick = []
onClick.append("@Override\n")
onClick.append("public void onClick(View v) {\n")
onClick.append("switch (v.getId()) {\n")
onItemSelected=[]

#Values to determie if we need to build out those sections.
hasButton = False
hasSpinner = False

#configure the parser
parser = etree.XMLParser(remove_blank_text=True)

#grab the file and parse it
file = open(sys.argv[1], "r")
tree = etree.parse(file,parser)
file.close()

events = ("start", "end")
context = etree.iterwalk(tree,events=events)
for action,elem in context:
   if action == 'start':
    attributes = elem.attrib
    for attribute in attributes:
        if attribute == "{%s}id" % namespace:
            try:
                elementId= None
                variableName = None
                identifier = attributes.get(attribute)
                elementId = identifier.split('/')[1]
                variableName=elementId.split('_')[1]
                if elem.tag == "TextView":
                    variableDefinition.append("TextView %s;\n" % variableName)
                    onCreate.append("%s = (TextView) this.findViewById(R.id.%s);\n" % (variableName, elementId))
                elif elem.tag == "CheckBox":
                    variableDefinition.append("CheckBox %s;\n" % variableName)
                    onCreate.append("%s = (CheckBox) this.findViewById(R.id.%s);\n" % (variableName, elementId))
                elif elem.tag == "EditText":
                    variableDefinition.append("EditText %s;\n" % variableName)
                    onCreate.append("%s = (EditText) this.findViewById(R.id.%s);\n" % (variableName, elementId))
                elif elem.tag == "Button":
                    variableDefinition.append("Button %s;\n" % variableName)
                    onCreate.append("%s = (Button) this.findViewById(R.id.%s);\n" % (variableName, elementId))
                    onCreate.append("%s.setOnClickListener(this);\n\n" % variableName)
                    onClick.append("case R.id.%s:\n" % elementId)
                    onClick.append("break;\n\n")
                    hasButton = True
                elif elem.tag == "LinearLayout":
                    variableDefinition.append("LinearLayout %s;\n" % variableName)
                    onCreate.append("%s = (LinearLayout) this.findViewById(R.id.%s);\n" % (variableName, elementId))
                elif elem.tag == "Spinner":
                    variableDefinition.append("Spinner %s;\n" % variableName)
                    variableDefinition.append("String %sSelected;\n" % variableName)
                    onCreate.append("%s = (Spinner) this.findViewById(R.id.%s);\n" % (variableName, elementId))
                    onCreate.append("ArrayAdapter<CharSequence> %sAdapter = ArrayAdapter.createFromResource(this ,R.array.#BK, android.R.layout.simple_spinner_item);\n" % variableName)
                    onCreate.append("%s.setAdapter(%sAdapter);\n"%(variableName,variableName))
                    onCreate.append("%s.setOnItemSelectedListener(new %sSelectedListener());\n\n" % (variableName, variableName))
                    onCreate.append("%s.setSelection(0);\n" % variableName)
                    onItemSelected.append("public class %sSelectedListener implements OnItemSelectedListener {\n" % variableName)
                    onItemSelected.append("public void onItemSelected(AdapterView<?> parent, View view, int pos, long id) {\n")
                    onItemSelected.append("%sSelected = parent.getItemAtPosition(pos).toString();}\n" % variableName)
                    onItemSelected.append("public void onNothingSelected(AdapterView<?> parent) {\n //Do Nothing \n}\n}")
                    hasSpinner = True
                elif elem.tag == "ToggleButton":
                  variableDefinition.append("ToggleButton %s;\n" % variableName)
                  onCreate.append("%s = (ToggleButton) this.findViewById(R.id.%s);\n" % (variableName, elementId))
                  onCreate.append("%s.setOnClickListener(this);\n\n" % variableName)
                  onClick.append("case R.id.%s:\n" % elementId)
                  onClick.append("break;\n\n")
                  hasButton = True
            
            except Exception as detail:
                print "Error: %s-%s - %s" %  (elem.tag, identifier, detail)

out = open(sys.argv[1]+".out", "w")
out.writelines(variableDefinition)
out.writelines(divider)
out.writelines(onCreate)
out.writelines(divider)
if hasButton == True:
    onClick.append("}\n}\n")
    out.writelines(onClick)
    out.writelines(divider)
if hasSpinner == True:
    out.writelines(onItemSelected)
out.close()
