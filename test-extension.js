const { chromium } = require("playwright");
const fs = require("node:fs");
const os = require("node:os");
const path = require("node:path");

const extensionPath = path.join(__dirname, "klaviyo-replace-button-extension");
const userDataDir = fs.mkdtempSync(
  path.join(os.tmpdir(), "klaviyo-replace-extension-test-")
);

const fixtureHtml = String.raw`<!doctype html>
<html>
  <head>
    <title>Edit Test | Klaviyo</title>
    <style>
      .ImageContainer-imagePreviewActions-B0BfB {
        display: flex;
      }

      .ImageContainer-imagePreviewActionButton-bl4JI {
        margin-right: 8px;
      }

      #image-preview-actions-45-replace {
        opacity: 0;
        pointer-events: none;
        order: 100;
        visibility: visible;
      }
    </style>
  </head>
  <body>
    <div class="ImageContainer-imagePreviewActions-B0BfB">
      <button
        id="image-preview-actions-45-crop"
        data-visible="true"
        class="Mixins-base-Y_5c1 Mixins-small-uzyOK Mixins-secondary-c0FUD Button-button-w3PcD ImageContainer-imagePreviewActionButton-bl4JI"
        type="button"
      >
        <span>Crop</span>
      </button>
      <button
        id="image-preview-actions-45-replace"
        data-visible="false"
        class="Mixins-base-Y_5c1 Mixins-small-uzyOK Mixins-secondary-c0FUD Button-button-w3PcD ImageContainer-imagePreviewActionButton-bl4JI"
        type="button"
        aria-hidden="true"
        tabindex="-1"
      >
        <span>Replace</span>
      </button>
      <button
        id="image-preview-actions-45-remix"
        class="Mixins-base-Y_5c1 Mixins-small-uzyOK Mixins-intelligence-primary-y1oMb Button-button-w3PcD TooltipWrapper"
        type="button"
      >
        <span>Remix</span>
      </button>
      <div id="image-preview-actions-45-end">Actions</div>
    </div>
  </body>
</html>`;

function assert(condition, message, details) {
  if (!condition) {
    const suffix = details ? `\n${JSON.stringify(details, null, 2)}` : "";
    throw new Error(`${message}${suffix}`);
  }
}

(async () => {
  const context = await chromium.launchPersistentContext(userDataDir, {
    headless: false,
    args: [
      `--disable-extensions-except=${extensionPath}`,
      `--load-extension=${extensionPath}`
    ]
  });

  try {
    const page = await context.newPage();
    await page.route("https://www.klaviyo.com/email-template-editor/smoke", (route) =>
      route.fulfill({
        contentType: "text/html",
        body: fixtureHtml
      })
    );

    await page.goto("https://www.klaviyo.com/email-template-editor/smoke", {
      waitUntil: "domcontentloaded"
    });

    await page.waitForFunction(() => {
      const button = document.querySelector(
        'button[id^="image-preview-actions-"][id$="-replace"]'
      );
      return (
        button &&
        button.getAttribute("data-klaviyo-replace-restored") === "true"
      );
    });

    const result = await page.evaluate(() => {
      const button = document.querySelector(
        'button[id^="image-preview-actions-"][id$="-replace"]'
      );
      const style = getComputedStyle(button);
      return {
        text: button.textContent.trim(),
        dataVisible: button.getAttribute("data-visible"),
        restored: button.getAttribute("data-klaviyo-replace-restored"),
        ariaHidden: button.getAttribute("aria-hidden"),
        tabindex: button.getAttribute("tabindex"),
        opacity: style.opacity,
        pointerEvents: style.pointerEvents,
        visibility: style.visibility,
        order: style.order,
        styleInstalled: Boolean(
          document.getElementById("klaviyo-replace-button-restorer-style")
        )
      };
    });

    assert(result.text === "Replace", "Replace button was not found.", result);
    assert(result.dataVisible === "true", "Replace button data-visible was not restored.", result);
    assert(result.restored === "true", "Replace button marker was not set.", result);
    assert(result.ariaHidden === null, "Replace button aria-hidden was not removed.", result);
    assert(result.tabindex === null, "Replace button tabindex was not removed.", result);
    assert(result.opacity === "1", "Replace button opacity was not restored.", result);
    assert(result.pointerEvents === "auto", "Replace button pointer-events was not restored.", result);
    assert(result.visibility === "visible", "Replace button visibility was not restored.", result);
    assert(result.order === "0", "Replace button order was not restored.", result);
    assert(result.styleInstalled, "Extension style tag was not installed.", result);

    console.log(JSON.stringify({ ok: true, result }, null, 2));
  } finally {
    await context.close();
    fs.rmSync(userDataDir, { recursive: true, force: true });
  }
})().catch((error) => {
  fs.rmSync(userDataDir, { recursive: true, force: true });
  console.error(error);
  process.exit(1);
});
