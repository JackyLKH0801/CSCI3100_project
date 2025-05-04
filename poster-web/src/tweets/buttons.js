import React from 'react'
import {apitweetAction} from './lookup';

export function ActionBtn(props){
    const {tweet, action, didPerfromAction} = props
    const likes = tweet.likes ? tweet.likes : 0
    const className = props.className ? props.className : `btn btn-primary btn-sm`
    const actionDisplay = action.display ? action.display : 'Action' 
    const display = action.type === 'like' ? `${likes} ${actionDisplay}` : actionDisplay
    const handleActionBackendEvent = (response, status) =>{
      if ((status === 200 || status === 201) && didPerfromAction){
        didPerfromAction(response, status)
      }
 
  }
    const handleClick = (event) => {
        event.preventDefault()
        apitweetAction(tweet.id, action.type, handleActionBackendEvent)
        }
    
    return <button className={className} onClick={handleClick}>{display}</button> 
  }