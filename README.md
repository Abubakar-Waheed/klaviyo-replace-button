# Klaviyo Replace Button Restorer

Small Chrome extension that restores Klaviyo's hidden image `Replace` button in the email template editor.

Klaviyo currently still renders the real button in the DOM, but hides it behind the three-dot image actions menu. This extension watches the editor and restores that original button so it is visible beside `Crop` and `Remix` again.

## Install

1. Open `chrome://extensions`.
2. Enable **Developer mode**.
3. Click **Load unpacked**.
4. Select the `klaviyo-replace-button-extension` folder from this repo.
5. Refresh the Klaviyo email template editor.
