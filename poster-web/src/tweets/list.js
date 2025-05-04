import React, {useEffect, useState} from 'react'
import { apitweetList} from './lookup';
import {Tweet} from './detail'
export function TweetsList(props){
    const [tweetsInit, setTweetsInit] =useState([])
    const [tweets, setTweets] = useState([])
    const [tweetsDidSet, setTweetsDidSet] = useState(false)
    console.log(props.newTweets)
    useEffect(() =>{
        const final = [...props.newTweets].concat(tweetsInit)
        if (final.length !== tweets.length){
            setTweets(final)
        }
    },[props.newTweets, tweetsInit, tweets.length])
    useEffect(() => {
      if (tweetsDidSet === false){
        const handleTweetListLookup = (response, status) => {
          if (status === 200) {
            setTweetsInit(response);
            setTweetsDidSet(true)
          } else {
              alert("error occured!",status,"response", response)
          }
        }
        apitweetList(props.username,handleTweetListLookup)
      }
     
    }, [tweetsInit, tweetsDidSet, setTweetsDidSet, props.username]);
    const handledidRetweet = (newTweet) =>{
      const updateTweetsInit = [...tweetsInit]
      updateTweetsInit.unshift(newTweet)
      setTweetsInit(updateTweetsInit)
      const updateFinalTweets = [...tweets]
      updateFinalTweets.unshift(newTweet)
      setTweets(updateFinalTweets)      
    }
    return tweets.map((item, index) => { 
      return <Tweet 
      tweet={item} 
      didRetweet= {handledidRetweet}
      className='my-5 py-5 border bg-white text-dark' 
      key={`${index}-{item.id}`}/>
    })
  
  }