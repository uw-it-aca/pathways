/**
 * Prevents typographic "widows" (a single word stranded alone on the
 * last line of a wrapped block of text) by replacing the whitespace
 * between the last two words with a non-breaking space.
 *
 * @param {string} str - The text to process.
 * @returns {string} The text with a non-breaking space before the last word.
 */
export function preventWidow(str) {
  if (typeof str !== "string" || !str.trim()) return str;
  return str.replace(/\s+([^\s]+)$/, "\u00A0$1");
}

export default {
  recentViewManager: function(title, url, campus){
    let currentRecentViews = JSON.parse(localStorage.getItem('recentViews')) || [];
    // add the new view to the front of the array
    if(!currentRecentViews.some(view => view.url === url)){
      currentRecentViews.unshift({title, url, campus});
    }
    currentRecentViews = currentRecentViews.slice(0, 5);

    localStorage.setItem('recentViews', JSON.stringify(currentRecentViews));
  }
};
