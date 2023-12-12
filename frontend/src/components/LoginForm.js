import React, {Component} from 'react';
import './LoginForm.css'

class LoginForm extends Component{

    state={
        login: '',
        password: '',
        logined: false,
        login_failed: false
    }

    send_login = async() => {
        await fetch("http://" + this.props.ip + ":3010/api/login", {
            method: 'POST',
            headers:{
                'content-type': 'application/json;charser=utf-8'
            },
            body: JSON.stringify({"login": this.state.login, "password": this.state.password})
        })
        .then(responce => {
            responce.json().then(res=>{
                console.log(res);
            if (res.body === 'OK'){
                this.props.set_login_status('logined');
                this.props.set_login_pass(this.state.login);
                this.setState({logined: true})
            }
            else{
                this.setState({login_failed: true})
            }
            })
            
        })
    }

    render(){
        return(
            <div className='LoginFormContainer'>
            <div className='LoginForm'>
                <span className='LoginLabel'>Login</span><br/>
                <input className='LoginFormInput LoginInput'    placeholder='Login' onChange={(event)=>{this.setState({login: event.target.value})}}></input><br/>
                <input className='LoginFormInput PasswordInput' placeholder='Password' type='password' onChange={(event)=>{this.setState({password: event.target.value})}}></input><br/>
                <button className='LoginButton' onClick={()=>{this.props.send_login()}}> Login </button><br/><br/>
                {(this.state.login_failed) ? <span className='LoginFailedLabel'>Login failed</span> :""}
            </div>
            </div>
        )
    }
}

export default LoginForm;