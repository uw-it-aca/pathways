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
