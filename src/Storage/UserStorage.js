import { extendObservable} from 'mobx';

class UserStorage{
    constructor(){
        extendObservable(this, {
            loading: true,
            isLoggedIn: false,
            username: ''
        })
    }
}

export default new UserStorage();