# Document Tools
## Structure
* Readme.md
* extract_xml.sh
* doc2csv.py
* csv2json.py
* test: directory for all experiment data
	* doc: storing original docx files
	* xml: storing xml files extracted from docx files
	* csv: storing csv files parsed from docx files
	* json: storing json files parsed from csv files

## extract_xml.sh
* Extracting word/document.xml and word/comments.xml from all given docx file
* Usage: 
	No parameters needed
* Result:  
	The extracted xml files will be as `/test/xml/{doc_name}_documents.xml` and `/test/xml/{doc_name}_comments.xml`

## doc2csv.py
* Parsing feedbacks including comments and revision from docx files and writing into csv files
* Usage:  
`python doc2csv.py [-D [DOCPATH]]`  
	DOCPATH: Path to original docx file, `test/doc/test.docx` as default path
* Result:  
	The output csv file will be as `/test/csv/{doc_name}.csv`

## csv2json.py
* Parsing feedbacks including comments and revision from csv files and writing into json files
* Usage:  
`python csv2json.py [-C [CSVPATH]]`  
	CSVPATH: Path to original csv file, `test/csv/test.csv` as default path
* Result:  
	The output json file will be as `/test/json/{csv_name}.csv`
