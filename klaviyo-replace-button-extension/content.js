(() => {
  const EDITOR_PATH = "/email-template-editor/";
  const STYLE_ID = "klaviyo-replace-button-restorer-style";
  const RESTORED_ATTR = "data-klaviyo-replace-restored";
  const REPLACE_BUTTON_SELECTOR =
    'button[id^="image-preview-actions-"][id$="-replace"]';

  let restoreQueued = false;

  function isEmailTemplateEditor() {
    return window.location.pathname.includes(EDITOR_PATH);
  }

  function installStyle() {
    if (document.getElementById(STYLE_ID)) {
      return;
    }

    const style = document.createElement("style");
    style.id = STYLE_ID;
    style.textContent = `
      ${REPLACE_BUTTON_SELECTOR}[${RESTORED_ATTR}="true"] {
        opacity: 1 !important;
        pointer-events: auto !important;
        visibility: visible !important;
        order: 0 !important;
      }
    `;
    document.documentElement.appendChild(style);
  }

  function restoreReplaceButton(button) {
    if (!(button instanceof HTMLButtonElement)) {
      return;
    }

    if (button.textContent.trim() !== "Replace") {
      return;
    }

    setAttributeIfChanged(button, "data-visible", "true");
    setAttributeIfChanged(button, RESTORED_ATTR, "true");
    removeAttributeIfPresent(button, "aria-hidden");
    removeAttributeIfPresent(button, "tabindex");
    setImportantStyle(button, "opacity", "1");
    setImportantStyle(button, "pointer-events", "auto");
    setImportantStyle(button, "visibility", "visible");
    setImportantStyle(button, "order", "0");
  }

  function setAttributeIfChanged(element, name, value) {
    if (element.getAttribute(name) !== value) {
      element.setAttribute(name, value);
    }
  }

  function removeAttributeIfPresent(element, name) {
    if (element.hasAttribute(name)) {
      element.removeAttribute(name);
    }
  }

  function setImportantStyle(element, property, value) {
    if (
      element.style.getPropertyValue(property) !== value ||
      element.style.getPropertyPriority(property) !== "important"
    ) {
      element.style.setProperty(property, value, "important");
    }
  }

  function restoreAllReplaceButtons() {
    if (!isEmailTemplateEditor()) {
      return;
    }

    installStyle();
    document
      .querySelectorAll(REPLACE_BUTTON_SELECTOR)
      .forEach(restoreReplaceButton);
  }

  function queueRestore() {
    if (restoreQueued) {
      return;
    }

    restoreQueued = true;
    window.requestAnimationFrame(() => {
      restoreQueued = false;
      restoreAllReplaceButtons();
    });
  }

  restoreAllReplaceButtons();

  const observer = new MutationObserver(queueRestore);
  observer.observe(document.documentElement, {
    childList: true,
    subtree: true,
    attributes: true,
    attributeFilter: [
      "aria-hidden",
      "data-visible",
      "style",
      "tabindex",
      RESTORED_ATTR
    ]
  });

  let lastPath = window.location.pathname;
  window.setInterval(() => {
    if (window.location.pathname !== lastPath) {
      lastPath = window.location.pathname;
      queueRestore();
    }
  }, 500);
})();
