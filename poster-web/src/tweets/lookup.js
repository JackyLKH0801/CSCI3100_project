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
export function apitweetFeed(callback, nextUrl) {
    let endpoint = "tweets/feed/"
    if (nextUrl !== null && nextUrl !== undefined){
        endpoint = nextUrl.replace("http://localhost:8000/api/", "")
    }
    backendLookup("GET", endpoint, callback)
}
export function apitweetList(username, callback, nextUrl) {
    let endpoint = "tweets/"
    if (username){
        endpoint =  `tweets/?username=${username}`
    }
    if (nextUrl !== null && nextUrl !== undefined){
        endpoint = nextUrl.replace("http://localhost:8000/api/", "")
    }
    backendLookup("GET", endpoint, callback)
}