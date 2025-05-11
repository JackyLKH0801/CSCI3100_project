import React, { useState} from 'react'
import { ActionBtn } from './buttons';

import {
  UserDisplay,
  UserPicture,
} from '../profiles'

export function ParentTweet(props){
    const {tweet} = props
    return tweet.parent ? <Tweet isRetweet retweeter={props.retweeter} hideActions className= {' '} tweet = {tweet.parent}/> : null
  }
  export function Tweet(props) {
      const {tweet, didRetweet, hideActions, isRetweet, retweeter} = props
      const [actionTweet, setActionTweet] = useState(props.tweet ? props.tweet : null) 
      let className = props.className ? props.className : 'col-10 mx-auto col-md-6'
      className = isRetweet === true ? `${className} p-2 border rounded` : className
      const path = window.location.pathname;
      const match = path.match(/(?<tweetid>\d+)/);
      const urlID = match ? match.groups.tweetid : -1;
      const isDetail = `${tweet.id}` === `${urlID}`
      const handleLink = (event) => {
        event.preventDefault()
        window.location.href = `/${tweet.id}`
      }
      const handlePerformAction = (newActionTweet, status) =>{
        if (status === 200){
          setActionTweet(newActionTweet)
        } else if (status === 201){
            if(didRetweet){
              didRetweet(newActionTweet)
            }
        }
      }
      const formatTimestamp = (timestamp) => {
        const date = new Date(timestamp);
        const now = new Date();
        const diffMs = now - date;
        const diffMins = Math.floor(diffMs / 60000);
        const diffHours = Math.floor(diffMins / 60);
        const diffDays = Math.floor(diffHours / 24);

        if (diffMins < 1) return 'Just now';
        if (diffMins < 60) return `${diffMins}m`;
        if (diffHours < 24) return `${diffHours}h`;
        if (diffDays < 7) return `${diffDays}d`;
        
        return date.toLocaleDateString(undefined, { month: 'short', day: 'numeric' });
      }
      
      return (
        <div className={`${className} tweet-card shadow-sm rounded p-3 mb-3`} 
          style={{
            background: 'linear-gradient(to bottom,rgb(221, 231, 240),rgb(191, 220, 250))',
            borderLeft: actionTweet && actionTweet.is_liked ? '3px solid rgba(224, 36, 94, 0.3)' : '3px solid transparent',
            transition: 'all 0.2s ease'
          }}>
        {isRetweet === true && (
          <div className='mb-2 retweet-header'>
            <i className="fa fa-retweet text-muted"></i> 
            <span className='small text-muted ml-1'>Retweeted by <UserDisplay user={retweeter} /></span>
          </div>
        )}
          
          <div className='d-flex'>
            <div className='tweet-avatar mr-2'>
              <UserPicture user={tweet.user} />
            </div>
            <div className='tweet-content'>
              <div className='tweet-header d-flex align-items-center justify-content-between'>
                <UserDisplay includeFullName user={tweet.user} />
                <span className="text-muted small ml-2">· {formatTimestamp(tweet.timestamp)}</span>
              </div>
              
              <div className='tweet-body my-2'>
                <p>{tweet.content}</p>
                {tweet.image && <img src={tweet.image} alt="Tweet media" className="img-fluid rounded mt-2" />}
              </div>
              
              <ParentTweet tweet={tweet} retweeter={tweet.user}/>
              
              <span className="ml-1 small">{actionTweet.likes || 0}{actionTweet.likes <= 1 ? " like" : " likes"}</span>
              {(actionTweet && hideActions !== true) && (
                <div className='tweet-actions d-flex mt-2'>
                  <div className="action-button text-center mx-2">
                    {actionTweet.is_liked ? (
                      <ActionBtn 
                        tweet={actionTweet} 
                        didPerfromAction={handlePerformAction} 
                        action={{type:"unlike", display:"Unlike"}}
                        className="btn btn-sm btn-outline-danger rounded-pill fixed-size-btn"
                      />
                    ) : (
                      <ActionBtn 
                        tweet={actionTweet} 
                        didPerfromAction={handlePerformAction} 
                        action={{type:"like", display:"Like"}}
                        className="btn btn-sm btn-outline-primary rounded-pill fixed-size-btn" 
                      />
                    )}
                  </div>
                  
                  <div className="action-button text-center mx-2">
                    <ActionBtn 
                      tweet={actionTweet} 
                      didPerfromAction={handlePerformAction} 
                      action={{type:"retweet", display:"Retweet"}}
                      className="btn btn-sm btn-outline-primary rounded-pill fixed-size-btn"
                    />
                  </div>
                  
                  {!isDetail && (
                    <div className="action-button text-center mx-2">
                      <button 
                        className='btn btn-sm btn-outline-primary rounded-pill fixed-size-btn' 
                        onClick={handleLink}>
                        View
                      </button>
                    </div>
                  )}
                </div>
              )}
            </div>
          </div>
        </div>
      )
      }
