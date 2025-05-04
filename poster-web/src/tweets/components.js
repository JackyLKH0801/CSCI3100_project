import React, {useState} from 'react'
import { TweetsList } from './list';
import {TweetCreate} from './create';
export function TweetsComponent(props){
  console.log("props are ", props)
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



