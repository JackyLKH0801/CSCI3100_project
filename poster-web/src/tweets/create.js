import React, {useState} from 'react'
import { apitweetCreate} from './lookup';

export function TweetCreate(props){
    const {didTweet} = props 
    const textAreaRef = React.createRef()
    const [charCount, setCharCount] = useState(0)
    const maxChars = 240
    const handleBackendUpdate = (response, status) => {
      if (status === 201) {
          didTweet(response)
          setCharCount(0)
      } else {
          console.log(response)
          alert("An error occurred while creating the tweet.")
      }
    }
    const handleChange = (event) => {
        setCharCount(event.target.value.length)
    }
    const handleSubmit = (event) => {
        event.preventDefault()
        const newVal = textAreaRef.current.value
        apitweetCreate(newVal, handleBackendUpdate)
        textAreaRef.current.value = ''
    }
    return (
        <div className={`${props.className} create-tweet-container`}>
            <form onSubmit={handleSubmit}>
                <div className="card shadow-sm">
                    <div className="card-body">
                        <textarea 
                            ref={textAreaRef} 
                            onChange={handleChange}
                            required={true} 
                            className="form-control border-0" 
                            placeholder="Type here"
                            style={{resize: "none", minHeight: "80px", fontSize: "1.1rem"}}
                        />
                        
                        <div className="d-flex justify-content-between align-items-center mt-3">
                            <div className={`char-counter ${charCount > maxChars ? 'text-danger' : 'text-muted'}`}>
                                {charCount > 0 && `${charCount}/${maxChars}`}
                            </div>
                            <button 
                                type="submit" 
                                className="btn btn-primary rounded-pill px-4"
                                disabled={charCount === 0 || charCount > maxChars}
                            >
                                Post
                            </button>
                        </div>
                    </div>
                </div>
            </form>
        </div>
    )
    // return <div className={props.className}>
    //     <form onSubmit = {handleSubmit}>
    //         <textarea ref={textAreaRef} required={true} className='form-control'>

    //         </textarea>
    //         <button type='submit' className='btn btn-primary my-3'>Post</button>
    // </form>
    // </div>
        }