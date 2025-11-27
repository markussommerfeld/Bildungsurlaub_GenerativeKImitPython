// Simple key capture for Dash Snake demo
// Sets the hidden input field with id 'key_input' to the key string when a key is pressed.
(function() {
  document.addEventListener('keydown', function(e) {
    try {
      var el = document.getElementById('key_input');
      if (!el) return;
      var key = e.key;
      // normalize arrow keys
      if (e.code && e.code.startsWith('Arrow')) {
        key = 'Arrow' + e.code.replace('Arrow', '');
      }
      el.value = key;
      // dispatch input event so Dash sees the change
      var event = new Event('input', { bubbles: true });
      el.dispatchEvent(event);
    } catch (err) {
      console.warn('keyboard capture error', err);
    }
  });
})();
