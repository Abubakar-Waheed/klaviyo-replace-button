# Klaviyo Replace Button Restorer

Tiny unpacked Chrome extension that restores Klaviyo's hidden image `Replace` button in the email template editor.

## Install

1. Open `chrome://extensions`.
2. Enable **Developer mode**.
3. Click **Load unpacked**.
4. Select this folder:

   `C:\Users\Abubakar\Desktop\Everything Homestead\Klaviyo Replace Button\klaviyo-replace-button-extension`

5. Refresh the Klaviyo email template editor.

## How It Works

Klaviyo still renders the real image replace button in the editor DOM as:

```css
button[id^="image-preview-actions-"][id$="-replace"]
```

The update hides it with `data-visible="false"`, `aria-hidden="true"`, `tabindex="-1"`, `opacity: 0`, `pointer-events: none`, and `order: 100`.

This extension watches the editor DOM and restores that original button back into the visible action row.
