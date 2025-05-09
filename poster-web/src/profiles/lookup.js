import {backendLookup} from '../lookup'

export function apiprofileDetail(username, callback) {
    backendLookup("GET", `profiles/${username}`, callback)
}

export function apiprofileFollowToggle(username, action, callback) {
    const data = {action: `${action && action}`.toLowerCase()}
    backendLookup("POST", `profiles/${username}/follow`, callback, data)
}