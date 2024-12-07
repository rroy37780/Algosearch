const express=require('express');
const {spawn}=require('child_process');
const app=express();

const PORT= process.env.PORT || 3000;   
app.listen(PORT,()=>{
    console.log("Server is running on Port "+PORT)
});

app.set('view engine','ejs');

app.use(express.static('public'));

app.get('/',(req,res)=>{
    res.render('index');
});

app.get('/results',(req,res)=>{
    const query=req.query.query
    console.log(query)
    const pythonProcess=spawn('python',['./tf-idf/query_handler.py',query])
    let output='';
    // Collect output from the Python script
    pythonProcess.stdout.on('data', (data) => {
        output += data.toString();
    });

    // Handle script completion
    pythonProcess.on('close', (code) => {
        if (code === 0) {
            try {
                const results = JSON.parse(output); // Assuming the Python script outputs JSON
                res.render('results',{results})
                // res.json({ results });
            } catch (error) {
                res.status(500).json({ error: 'Failed to parse Python script output' });
            }
        } else {
            res.status(500).json({ error: 'Python script failed to execute' });
        }
    });

    // Handle errors
    pythonProcess.stderr.on('data', (data) => {
        console.error(`Error: ${data.toString()}`);
    });
    // res.render('results');
});

app.get('/search',(req,res)=>{
    const  query=req.query.query;

    console.log(query)
    const pythonProcess=spawn('python',['./tf-idf/query_handler.py',query])
    let output='';
    // Collect output from the Python script
    pythonProcess.stdout.on('data', (data) => {
        output += data.toString();
    });

    // Handle script completion
    pythonProcess.on('close', (code) => {
        if (code === 0) {
            try {
                const results = JSON.parse(output); // Assuming the Python script outputs JSON
                res.json(results)
                // res.json({ results });
            } catch (error) {
                res.status(500).json({ error: 'Failed to parse Python script output' });
            }
        } else {
            res.status(500).json({ error: 'Python script failed to execute' });
        }
    });

    // Handle errors
    pythonProcess.stderr.on('data', (data) => {
        console.error(`Error: ${data.toString()}`);
    });
    // res.render('results');
})
