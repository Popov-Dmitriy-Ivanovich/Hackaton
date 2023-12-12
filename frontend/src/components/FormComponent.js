import React, {Component} from 'react'
import SeparateLine from './SeparateLine'
import './FormComponent.css'


class FormComponent extends Component{
    state={
        subforms: []
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
        // fetch('http://'+this.props.ip+':3010/api/form/'+this.props.form_path)
        // .then(res => res.json())
        // .then(
        //     (result) => {
        //         this.setState({
        //             loaded: true,
        //             subforms: result.data,
        //             choices: {}
        //         });
        //     },
        //     (error) => {
        //         this.setState({
        //             loaded: true,
        //             error
        //         })
        //     }
        // )
        this.setState({subforms: this.props.subforms})
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
            <div>
                <ul className="Form_ul">
                    {this.state.subforms.map((subform)=>(
                        <li>
                            <div className='subform_container'>
                            {subform.text}<br/>
                            {
                                <ul style={{listStyle: 'none'}}>
                                    {subform.buttons.buttons_texts.map((text)=>(
                                        <li>
                                            <input
                                                type={subform.buttons.buttons_type} 
                                                name={subform.text} 
                                                onChange={
                                                    (subform.buttons.buttons_type==="radio") ? 
                                                        ()=>this.buttons_listener(subform.text, text) 
                                                    : (subform.buttons.buttons_type==="checkbox") ? 
                                                        ()=>this.buttons_listener(subform.text, this.state.choices[subform.text]==='+' ? '-' : '+') 
                                                    : (subform.buttons.buttons_type==="text") ? 
                                                        (event)=>this.buttons_listener(subform.text, event.target.value) 
                                                    :
                                                        ()=>{}}
                                            >
                                            </input>{text}
                                        </li>
                                    ))}
                                </ul>
                            }
                            <SeparateLine/>
                            </div>
                        </li>
                    ))}
                </ul>
                <ul>
                    {(this.state.choices!=null) ? Object.keys(this.state.choices).map(key => (<li>{key} {this.state.choices[key]}</li>)) : ''}
                </ul>

                    <div className="PDF_button_container"><div id="get_pdf_div" onClick={this.SendLEDForm}>Get PDF</div></div>

            </div>
        )
    }

}
export default FormComponent;