import React, {Component} from 'react'
import './FormComponent.css'


class FormComponent extends Component{
    state={
        subforms: [],
        choices: [],
        text_inputs: {}
    }
    constructor(props){
        super(props);
    }

    buttons_listener = (text, value) => {
        let tmp=this.state.choices;
        tmp[text]=value;
        this.setState({choices: tmp});
    }

    componentDidMount() {
        fetch('http://'+this.props.ip+':80/api/get_profile_form/')
        .then(res => res.json())
        .then(
            (result) => {
                this.setState({
                    loaded: true,
                    subforms: result,
                    choices: {}
                });
            },
            (error) => {
                this.setState({
                    loaded: true,
                    error
                })
            }
        )
        // this.setState({subforms: this.props.subforms})
    }

    change_text_input = (key, new_text)=>{
        let tmp = this.state.text_inputs;
        tmp[key] = new_text;
        this.setState({text_inputs: tmp})
    }

    SendLEDForm = async() => {
        await fetch("http://" + this.props.ip + ":3010/api/response/LED_form", {
            method: 'POST',
            headers:{
                'content-type': 'application/json;charser=utf-8'
            },
            body: JSON.stringify({
                choices: this.state.choices,
                login: this.props.login
            })
        })
        .then(responce => {
            if(responce.ok){
                responce.json().then(json=>{
                    window.open("http://" + this.props.ip + ":3010/"+json.body)
                })
            }
            else{
                console.log("bad responce");
            }
        })
    }

    render(){
        return(
            <div className='FormContainer'>
                <ul className="Form_ul">
                    {this.state.subforms.map((subform)=>(
                        <li>
                            <div className='subform_container'>
                            <div className='subform_lable'>{subform.text}</div>
                            {
                                <ul style={{listStyle: 'none'}}>
                                    {subform.buttons.buttons_texts.map((text)=>(
                                        <li>
                                            <input
                                                className='FormInput'
                                                type={subform.buttons.buttons_type} 
                                                name={subform.text} 
                                                onChange={
                                                    (subform.buttons.buttons_type==="radio") ? 
                                                        ()=>this.buttons_listener(subform.text, text) 
                                                    : (subform.buttons.buttons_type==="checkbox") ? 
                                                        ()=>this.buttons_listener(subform.text, this.state.choices[subform.text]==='+' ? '-' : '+') 
                                                    : (subform.buttons.buttons_type==="text") ? 
                                                        (event)=>{this.buttons_listener(subform.text, event.target.value); this.change_text_input(subform.text, event.target.value)} 
                                                    :
                                                        ()=>{}}
                                            >
                                            </input>{text}
                                        </li>
                                    ))}
                                </ul>
                            }
                            </div>
                        </li>
                    ))}
                </ul>
                

            </div>
        )
    }

}
export default FormComponent;