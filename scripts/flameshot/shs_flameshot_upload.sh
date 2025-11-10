#!/bin/bash
# Flameshot command to take a screenshot and save it to a temporary file, then upload it to our SelfhostScreenshot. Highly recommend to create a shortcut in KDE (for example 'Meta+C') for a nice usage
tempfile=$(mktemp /tmp/screenshot.XXXXXX.png)
flameshot gui -r > "$tempfile"

# Custom URL for our SelfhostScreenshot
url=https://localhost:7070


# Check if the temporary file was created and is not empty
if [ ! -s "$tempfile" ]; then
    echo "Screenshot failed or was cancelled."
    rm -f "$tempfile"
    exit 1
fi

response=$(curl -s -F "file=@$tempfile" -H "X-API-Key: XXXXXX-XXXXXX-XXXXXX-XXXXXX" $url"/upload")

echo $response
link=$(echo $response | jq -r '.link')
echo "Upload link: $url$link"


# Open the response link in the default browser
if [ -n "$link" ]; then
    xdg-open "$url$link"
else
    echo "Failed to upload the image."
fi
