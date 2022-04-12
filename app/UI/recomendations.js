const recomendations = {template: `
<div>
  
    <div style="
        margin-top:13%; 
        padding: 20px; "
    >   
        <div v-for="doc in documents" style="margin-top: 2%;">
            <div class="card" style="margin-left: 4%; 
            margin-right: 4%;">
                <div class="card-body">
                <h5 class="card-title"> {{doc[1]}} </h5>
                <h6 class="card-subtitle text-muted"> by {{doc[2]}} </h6>
                <a :href="'https://www.gutenberg.org/ebooks/' + doc[0]" class="card-link">Gutenberg link</a>
                </div>
            </div>
        </div>
    </div>
</div>

`,



data(){
    return {
        documents:[]
    } 
},
methods:{
    refreshData(){console.log(this.keyword);
        this.documents=[];
        if(this.keyword !== "")
            axios.get(variables.API_URL+"recomendations")
            .then((response) => {
                this.documents=response.data;
                console.log(response.data[0]);
            });
    }
}, 
mounted:function(){ this.refreshData(); }       


}

