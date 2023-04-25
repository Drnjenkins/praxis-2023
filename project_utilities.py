import os
import fnmatch
import subprocess

def upload_to_s3():
    bucket = "praxis-2023-html-output"
    website = f"http://{bucket}.s3-website-us-west-2.amazonaws.com"

    # Use the fnmatch module to find all files in the current directory that end in ".html"
    file_list = []
    for root, dirnames, filenames in os.walk("."):
        for filename in fnmatch.filter(filenames, '*.html'):
            file_list.append(os.path.join(root, filename))

    # Sort the file list alphabetically
    file_list.sort()

    # Create the HTML file and write the header
    with open(os.path.join(".", 'index.html'), 'w') as f:
        f.write('''<html>
            <head>
                <title>Praxis 2023 HTML Output</title>
                <style>
                    table {
                        border-collapse: collapse;
                        width: 100%;
                    }
                    th, td {
                        text-align: left;
                        padding: 8px;
                    }
                    th {
                        background-color: #007bff;
                        color: #fff;
                        font-weight: bold;
                    }
                    tr:nth-child(even) {
                        background-color: #f2f2f2;
                    }
                    tr:hover {
                        background-color: #ddd;
                    }
                </style>
            </head>
            <body>
                <table>
                    <tr><th>Name</th><th>Size</th></tr>\n
        ''')

        # Loop through each file and add a row to the table
        for file_name in file_list:
            if file_name in ['./index.html']:
                continue

            file_size = os.path.getsize(file_name)
            f.write(f'<tr><td><a href="{website}/{file_name}" target="_blank" rel="noopener noreferrer">{file_name}</a></td><td>{int(file_size / 1048576)} MB</td></tr>\n')

        # Write the footer and close the file
        f.write('</table></body></html>')

    command = ["aws", "s3", "sync", ".", f"s3://{bucket}", "--exclude", "*", "--include", "*.html", "--no-progress"]

    # Run the command and wait for it to complete
    output = subprocess.run(command, capture_output=True, text=True)

    # Print the output
    print(output.stdout)
    print('fin')