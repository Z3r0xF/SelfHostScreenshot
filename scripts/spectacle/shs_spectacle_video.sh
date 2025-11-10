#!/bin/bash
#Uses KDE Spectacle to record a video and uploads it to our SelfhostScreenshot. Highly recommend to create a shortcut in KDE (for example 'Meta+R') for a nice usage
video_directory="$HOME/Videos/SelfhostScreenshot"

#Create the directory if it doesn't exist
mkdir -p "$video_directory"

spectacle --record r -b -n -o "$video_directory/screenshot_$(date +%Y%m%d_%H%M%S).mp4"

#Wait till file is created
sleep 1

#Take the latest created file with extension .mp4
video_file=$(ls -t "$video_directory"/*.mp4 | head -n 1)

# URL
url="https://localhost:7070"

#Upload to SelfhostScreenshot
response=$(curl -s -F "file=@$video_file" -H "X-API-Key: XXXXXX-XXXXXX-XXXXXX-XXXXXX" "$url/upload")


link=$(echo $response | jq -r '.link')

echo "Upload link: $url$link"

# Open link in the default browser
if [ -n "$link" ]; then
    xdg-open "$url$link"
else
    echo "Failed to upload the video."
fi