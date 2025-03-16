import requests
import os

groupsDict={62614:"Digitallab_01__17:20-18:00",62615:"digitallab_02__18:00-18:40",62616:"digitallab_03__18:40-19:20",
           62617:"digitallab_04__19:20-20:00",62618:"digitallab_05__20:00-20:40",62619:"digitallab_06__20:40-21:20",
           62610:"linuxlab_01__15:20-16:00",62611:"linuxlab_02__16:00-16:40",62612:"linuxlab_03__16:40-17:20",
           62613:"linuxlab_04__17:20-18:00",62603:"winlab_01__17:20-18:00",62604:"winlab_02__18:00-18:40",
           62605:"winlab_03__18:40-19:20",62606:"winlab_04__19:20-20:00",62607:"winlab_05__20:00-20:40",
           62608:"winlab_06__20:40-21:20",62741:"winlab_04 19:20-20:00_extra_time"}


outputDir = "xls"
if not os.path.exists(outputDir):
    os.makedirs(outputDir)

# Define the cookie and headers
cookies = {
    'PHPSESSID': 'ai644mem2girqvaegq38bmgo18'  # Replace with your actual session ID
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
}

for aGRoupId in groupsDict:
    
    groupName=groupsDict[aGRoupId]
    file_url = f"https://eclass.uoa.gr/modules/group/dumpgroup.php?course=DI507&group_id={aGRoupId}"
    filename = os.path.join(outputDir, f"{groupName}.xlsx") 

    
    response = requests.get(file_url, cookies=cookies, headers=headers, stream=True) # Make the request
    if response.status_code == 200: # Check if the request was successful
        with open(filename, "wb") as file:
            for chunk in response.iter_content(chunk_size=1024):
                file.write(chunk)

        print(f"Download successful! File saved as {filename}")
    else:
        print(f"Failed to download file. Status code: {response.status_code}")
