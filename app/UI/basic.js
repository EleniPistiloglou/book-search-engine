const basic = {template: `
<div>
    <div style="
        margin-top:13%; 
        padding: 20px;
        margin-left: 6%; 
        margin-right: 6%;
        border: 6px solid #212121;"
    >
        <h3 style="margin-bottom:20px;">Welcome to the basic search !</h3>

        <div>
            <div style="display: flex;
            justify-content: center;
            margin: 100px 100px 100px 100px;">
                
                <br/><br/>

                <input 

                    placeholder="Type a keyword"
                    type="text" id="keyword" 
                    v-model="keyword"
                    style="
                        width: 50%;
                        border: none;
                        border-radius: 0;
                        border-bottom: 3px solid black;
                        background: none;
                        color: #333;
                        font-size: 26px;" 
                    />
            </div>

        </div>

        <div style="text-align: right; margin-top: 50px; margin-right: 10px;">

            <button 
                @click="refreshData()"
                style="
                    width: 300px;
                    height: 100px;
                    border: none;
                    border-radius: 0;
                    background: none;
                    font-size: 26px;"
            >Go!</button>

        </div>

    </div>  

    <div v-for="doc in documents" style="margin-top: 2%;">
        <div class="card" style="margin-left: 6%; 
        margin-right: 6%;">
            <div class="card-body">
            <h5 class="card-title"> {{doc[0]}} </h5>
            <h6 class="card-subtitle text-muted"> {{doc[1]}} </h6>
            <p class="card-text">Welcome to Tutlane. Its card sample text.</p>
            <a href="#" class="card-link">Link1</a>
            <a href="#" class="card-link">Link2</a>
            </div>
        </div>
    </div>

</div>

`,



data(){
    return {
        documents:[], keyword:"" 
    } 
},
methods:{
    refreshData(){console.log(this.keyword);
        if(this.keyword !== "")
            axios.get(variables.API_URL+"basic/"+this.keyword)
            .then((response) => {
                this.documents=response.data;
                console.log(response.data[0]);
            });
    }
}, 
mounted:function(){ this.refreshData(); }       


}

