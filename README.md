# MFCDialogCopyTool
I got really fed up with manually copying over dialog resources from one file to another so I made a simple python script to do it for me. 

# Usage
It is highly advised you take a backup of your resource.h and project.rc files before using this tool as it has a high chance of corrupting the result if used incorrectly. 

To use the tool perform the following
1. Create an empty dialog in the target project. This is used for identifying where in the file to paste the dialog once copied. 
2. Close Visual Studio (target solution)
3. Run the command with relevent arguments to copy the dialog from source to destination
4. Open ResOrg (not in Visual Studio) and renumber the resulting resource.h file, this program assigns all new symbols ID=-1, you are responsible for running ResOrg to get a valid range of symbols
5. You an now safely open Visual Studio and the dialog resource will have been copied over 

Just run the command as below. It takes two required arguments. 
`usage: main.py [-h] [--dest_h DEST_H] [--dest_rc DEST_RC] dlg src_rc`
* **dlg**: The name of the dialog
* **src_rc**: The name of the source project.rc MFC file. This is where the dialog will be extracted from.
* **--dest_h**: The name of the target resource.h file. This is where all resulting new symbols will be pasted. If no file is provided then it simply will not paste in missing symbols.
* **--dest_rc**: This is the file where the resulting dialog will be pasted
