import React from 'react';
import {StrictMode} from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';
import {ProfileBadgeComponent} from './profiles'
// import reportWebVitals from './reportWebVitals';
import {FeedComponent, TweetsComponent, TweetDetailComponent} from './tweets';
const rootContainer =document.getElementById('root');
if (rootContainer){
  const appEl = ReactDOM.createRoot(rootContainer)
  appEl.render(
    <StrictMode>
      <App />
      </StrictMode>
  )
}
const postContainer = document.getElementById('POSTer')
if (postContainer){
  console.log(postContainer.dataset); 
const tweetsEl = ReactDOM.createRoot(postContainer); //note that the ReactDOM is postContainer and not tweetsEl
console.log(postContainer.dataset);
tweetsEl.render(
  <StrictMode>
<TweetsComponent 
  username={postContainer.dataset.username} 
  canPost={postContainer.dataset.canPost}  />

</StrictMode>
);
}

const feedContainer = document.getElementById('POSTer-feed')
if (feedContainer){
  console.log(feedContainer.dataset); 
const tweetsFeedEl = ReactDOM.createRoot(feedContainer); //note that the ReactDOM is postContainer and not tweetsEl
console.log(feedContainer.dataset);
tweetsFeedEl.render(
  <StrictMode>
<FeedComponent 
  username={feedContainer.dataset.username} 
  canPost={feedContainer.dataset.canPost}  />

</StrictMode>
);
}

const tweetDetailElements = document.querySelectorAll(".POSTer-detail")
tweetDetailElements.forEach(container=>{
 const root = ReactDOM.createRoot(container);
 root.render(
  React.createElement(TweetDetailComponent, container.dataset, container)
 )

})

const userProfileBadgeElements = document.querySelectorAll(".POSTer-profile-badge")
userProfileBadgeElements.forEach(container=>{
 const root = ReactDOM.createRoot(container);
 root.render(
  React.createElement(ProfileBadgeComponent, container.dataset, container)
 )

})
// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
