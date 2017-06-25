cd test/doc
FILES=*.docx
for file in $FILES
do
	suffix=.docx
	name=${file%.docx}
	echo $name

	echo "Extracting $file ..."
	unzip $file
	echo "Copying xml to xml/"
	mv word/document.xml ../xml/${name}_document.xml
	mv word/comments.xml ../xml/${name}_comments.xml
	echo "Removing redundant files"
	find . ! -name '*.docx' -delete
done

cd ../original_doc
FILES=*.docx
for file in $FILES
do
	suffix=.docx
	name=${file%.docx}
	echo $name

	echo "Extracting $file ..."
	unzip $file
	echo "Copying xml to original_xml/"
	mv word/document.xml ../original_xml/${name}_document.xml
	echo "Removing redundant files"
	find . ! -name '*.docx' -delete
done

cd ..