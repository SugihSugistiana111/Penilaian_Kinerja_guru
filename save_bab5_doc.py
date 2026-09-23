import os
import shutil
import time

# Try to use pywin32 to close and reload BAB V.docx if open
try:
    import win32com.client
    word = win32com.client.Dispatch("Word.Application")
    for doc in word.Documents:
        if "BAB V.docx" in doc.FullName or "BAB V" in doc.Name:
            print(f"Closing open document in Word: {doc.FullName}")
            doc.Close(SaveChanges=False)
except Exception as e:
    print(f"COM dispatch note: {e}")

time.sleep(1)

# Now copy BAB_V_temp.docx to BAB V.docx
try:
    shutil.copyfile("BAB_V_temp.docx", "BAB V.docx")
    print("SUCCESS: BAB V.docx has been updated successfully!")
except Exception as e:
    print(f"Copy failed: {e}")
