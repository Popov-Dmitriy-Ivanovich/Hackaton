import React, {Component} from 'react';
import './LoginForm.css'
// import { Agent } from './https-browserify/index';


class LoginForm extends Component{

    state={
        login: '',
        password: '',
        name: '',
        logined: false,
        login_failed: false,
        register: false
    }

    send_login = async() => {
          
        await fetch(this.props.main_host + this.props.login_route, {
            // agent: new Agent({
            //     rejectUnauthorized: false
            //  }),
            method: 'POST',
            headers:{
                'content-type': 'application/json;charser=utf-8'
            },
            body: JSON.stringify({"login": this.state.login, "password": this.state.password}),
        })
        .then(responce => {
            responce.json().then(res=>{
            if (res.status === 'OK'){
                this.props.send_login(this.state.login, this.state.password);
                this.setState({logined: true})
            }
            else{
                this.setState({login_failed: true})
            }
            })
            
        })
    }

    register = () => {
        this.setState({register: true})
    }

    send_register = async() => {
          
        await fetch(this.props.main_host + this.props.register_route, {
            // agent: new Agent({
            //     rejectUnauthorized: false
            //  }),
            method: 'POST',
            headers:{
                'content-type': 'application/json;charser=utf-8'
            },
            body: JSON.stringify({"login": this.state.login, "password": this.state.password, "name": this.state.name})
        })
        .then(responce => {
            responce.json().then(res=>{
            if (res.status === 'OK'){
                this.setState({register: false})
                
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
                    
                    <span   style={{display: !this.state.register ? '' : 'none' }}    className='LoginLabel'>Login</span><br/>
                    <span   style={{display:  this.state.register ? '' : 'none' }}    className='LoginLabel'>Register</span><br/>
                    <input                                                            className='LoginFormInput LoginInput'    placeholder='Login' onChange={(event)=>{this.setState({login: event.target.value})}}></input><br/>
                    <input                                                            className='LoginFormInput PasswordInput' placeholder='Password' type='password' onChange={(event)=>{this.setState({password: event.target.value})}}></input><br/>
                    <input  style={{display:  this.state.register ? '' : 'none' }}    className='LoginFormInput NameInput'     placeholder='Name'                     onChange={(event)=>{this.setState({name: event.target.value})}}></input><br/>
                    <button style={{display: !this.state.register ? '' : 'none' }}    className='LoginButton'    onClick={()=>{this.send_login()}}> Login    </button><br/><br/>
                    <button style={{display: !this.state.register ? '' : 'none' }}    className='RegisterButton' onClick={()=>{this.register()}  }> Register </button><br/>
                    <button style={{display:  this.state.register ? '' : 'none' }}    className='RegisterButton' onClick={()=>{this.send_register()}  }> Register </button><br/>
                    {(this.state.login_failed&&(!this.state.register)) ? <span className='LoginFailedLabel'>Login failed</span> :""}
                </div>
            </div>
        )
    }
}

export default LoginForm;