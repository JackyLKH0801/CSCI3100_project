import {backendLookup} from '../lookup'

export function apitweetCreate(data, callback) {
    backendLookup("POST", "tweets/create/", callback, {content: data})
}
export function apitweetAction(tweetid, action, callback) {
    const data = {id: tweetid, action:action}
    backendLookup("POST", "tweets/action/", callback, data)
}
export function apitweetDetail(tweetid, callback) {
    backendLookup("GET", `tweets/${tweetid}`, callback)
}
export function apitweetList(username, callback) {
    let endpoint = "tweets/"
    if (username){
        endpoint =  `tweets/?username=${username}`
    }
   
    backendLookup("GET", endpoint, callback)
}