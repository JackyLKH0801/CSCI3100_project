import React from 'react'
import { apitweetCreate} from './lookup';

export function TweetCreate(props){
    const {didTweet} = props 
    const textAreaRef = React.createRef()
    const handleBackendUpdate = (response, status) => {
      if (status === 201) {
          didTweet(response)
      } else {
          console.log(response)
          alert("An error occurred while creating the tweet.")
      }
    }
    const handleSubmit = (event) => {
        event.preventDefault()
        const newVal = textAreaRef.current.value
        apitweetCreate(newVal, handleBackendUpdate)
        textAreaRef.current.value = ''
    }
    return <div className={props.className}>
        <form onSubmit = {handleSubmit}>
            <textarea ref={textAreaRef} required={true} className='form-control'>

            </textarea>
            <button type='submit' className='btn btn-primary my-3'>Post</button>
    </form>
    </div>
        }