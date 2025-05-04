import React from 'react';
import { StrictMode } from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';
// import reportWebVitals from './reportWebVitals';
import { TweetsComponent } from './tweets';
const rootContainer =document.getElementById('root');
if (rootContainer){
  const appEl = ReactDOM.createRoot(rootContainer)
  appEl.render(
    <StrictMode>
      <App />
      </StrictMode>
  )
}
const container = document.getElementById('POSTer')
if (container){
  console.log(container.dataset); 
const tweetsEl = ReactDOM.createRoot(container); //note that the ReactDOM is container and not tweetsEl
console.log(container.dataset)
tweetsEl.render(
  <StrictMode>
<TweetsComponent 
  username={container.dataset.username} 
  canPost={container.dataset.canPost}  />

</StrictMode>
);
}

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
