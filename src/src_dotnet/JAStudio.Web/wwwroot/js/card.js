// Card interaction scripts for Blazor iframe
// Right-click selection for clipboard elements and audio player setup

function initializeCardInteractions() {
   function selectText(element) {
      const range = document.createRange();
      range.selectNodeContents(element);
      const selection = window.getSelection();
      selection.removeAllRanges();
      selection.addRange(range);
   }

   document.querySelectorAll('.clipboard, ja, .headword-term, rad, radical, voc, vocab, kan, kanji, read, reading')
      .forEach(function (element) {
         if (element.dataset.rightClickInitialized) return;
         element.dataset.rightClickInitialized = 'true';

         element.addEventListener('mousedown', event => {
            if (event.button === 2) {
               const selection = window.getSelection();
               const selectedText = selection.toString();

               if (!selectedText || !element.contains(selection.anchorNode)) {
                  selectText(element);
               }
            }
         });
      });

   setupAudioPlayers();
}

function setupAudioPlayers() {
   const initializedClassName = "initialized";
   const audioElements = document.getElementsByTagName('audio');

   for (let i = 0; i < audioElements.length; i++) {
      const audio = audioElements[i];
      const button = audio.nextElementSibling;
      if (button && audio.getAttribute('src') && button.classList.contains('play-button') && !button.classList.contains(initializedClassName)) {
         button.classList.add(initializedClassName);
         button.innerHTML = '▶';

         button.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            const audioElement = this.previousElementSibling;
            if (audioElement.paused) {
               audioElement.play();
               this.innerHTML = '⏸︎';
            } else {
               audioElement.pause();
               this.innerHTML = '▶';
            }
         });

         audio.parentNode.insertBefore(button, audio.nextSibling);

         audio.addEventListener('ended', function() { this.nextElementSibling.innerHTML = '▶'; });
      }
   }
}

// Initialize when DOM is ready, and re-initialize after Blazor enhanced navigations
if (document.readyState === 'loading') {
   document.addEventListener('DOMContentLoaded', initializeCardInteractions);
} else {
   initializeCardInteractions();
}

// Re-initialize after Blazor Server re-renders content
Blazor.addEventListener('enhancedload', initializeCardInteractions);

// Note link click handling.
// In Anki's iframe: call the server API to open in the system browser (avoids navigating the review iframe).
// In a regular browser: let the default <a> behavior proceed (same tab, or new tab on ctrl/shift+click).
function setupNoteLinks() {
   const isInIframe = window.parent !== window;
   if (!isInIframe) return;

   document.addEventListener('click', function(event) {
      const link = event.target.closest('.note-link');
      if (!link) return;

      event.preventDefault();
      const noteType = link.dataset.noteType;
      const noteId = link.dataset.noteId;
      if (noteType && noteId) {
         fetch('/api/open-in-browser/' + encodeURIComponent(noteType) + '/' + encodeURIComponent(noteId));
      }
   });
}

setupNoteLinks();
