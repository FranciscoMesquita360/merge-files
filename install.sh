# install.sh
#!/bin/bash
REPO="FranciscoMesquita360/merge-files"
BINARY_NAME="merge-linux"
INSTALL_DIR="/usr/local/bin"

echo "🚀 Installing 'merge' command..."

# 1. Get the latest release URL
URL=$(curl -s https://api.github.com/repos/$REPO/releases/latest | grep "browser_download_url" | grep "$BINARY_NAME" | cut -d '"' -f 4)

if [ -z "$URL" ]; then
    echo "❌ Error: Could not find the binary."
    exit 1
fi

# 2. Download and rename it immediately to 'merge'
curl -L -o merge "$URL"

# 3. Give execution permission
chmod +x merge

# 4. Move to PATH
sudo mv merge $INSTALL_DIR/
echo "✅ Successfully installed! You can now use the command: merge"