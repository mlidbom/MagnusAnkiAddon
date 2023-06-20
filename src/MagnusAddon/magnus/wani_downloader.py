import os
import requests
from aqt import mw

class FileDownloadError(Exception):
    pass

class WaniDownloader:
    def media_dir(self) -> str : return mw.col.media.dir()

    def download_file(url, directory) -> str:
        response = requests.get(url)

        if response.status_code == 200:
            filename = WaniDownloader.get_filename_from_headers(response)
            file_path = os.path.join(directory, filename)
            with open(file_path, 'wb') as file:
                file.write(response.content)
        else:
            raise FileDownloadError("{} -> {}".format(url, directory))

    def get_filename_from_headers(response):
        content_disposition = response.headers.get('content-disposition')

        if content_disposition:
            filename = content_disposition.split('filename=')[1].strip('"')
            return filename

        # If no filename found in the headers, extract from the URL
        return response.url.split('/')[-1]
