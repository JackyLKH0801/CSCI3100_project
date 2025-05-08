import React, {useEffect, useState} from 'react'
import {TweetsList} from './list';
import {TweetsFeedList} from './feed'; 
import {TweetCreate} from './create';
import {apitweetDetail} from './lookup';
import { Tweet } from './detail';

export function FeedComponent(props){
  const [newTweets, setNewTweets] = useState([])
  const canPost = props.canPost === 'false' ? false : true
  const handlenewTweet = (newTweet) => {
    let tempNewTweets = [...newTweets]
    tempNewTweets.unshift(newTweet)
    setNewTweets(tempNewTweets)
  }

  return <div className={props.className}>
      {
      canPost === true &&<TweetCreate didTweet={handlenewTweet} className='col-12 mb-3' />
      }
  <TweetsFeedList newTweets={newTweets} {...props}/>
  </div>
}
export function TweetsComponent(props){
    const [newTweets, setNewTweets] = useState([])
    const canPost = props.canPost === 'false' ? false : true
    const handlenewTweet = (newTweet) => {
      let tempNewTweets = [...newTweets]
      tempNewTweets.unshift(newTweet)
      setNewTweets(tempNewTweets)
    }

    return <div className={props.className}>
        {
        canPost === true &&<TweetCreate didTweet={handlenewTweet} className='col-12 mb-3' />
        }
    <TweetsList newTweets={newTweets} {...props}/>
    </div>
}
export function TweetDetailComponent(props){
    const {tweetId} = props
    const [didLookup,setDidLookup] = useState(false)
    const [tweet, setTweet] = useState(null)
    const handleBackendLookup = (response,status) =>{
      if (status === 200){
        setTweet(response)
      }
      else {
        alert("Cant find post.")
      }
    }
    useEffect(()=>{
        if (didLookup === false){
          apitweetDetail(tweetId, handleBackendLookup)
          setDidLookup(true)
        }
    },[tweetId, didLookup, setDidLookup, handleBackendLookup])
  return tweet === null ? null : <Tweet tweet= {tweet} className= {props.className} />
}


