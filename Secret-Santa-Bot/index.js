const { Client, Intents, MessageActionRow, MessageButton } = require('discord.js');
const { token } = require('./config.json');
const wait = require('util').promisify(setTimeout);

const botIntents = new Intents();
botIntents.add(Intents.FLAGS.GUILD_PRESENCES, Intents.FLAGS.GUILD_MEMBERS, Intents.FLAGS.DIRECT_MESSAGES);

const client = new Client({ intents: botIntents });

client.once('ready', () => {
	console.log('Ready!');
});

client.on('interactionCreate', async interaction => {
    if(!interaction.isCommand()) return;

    const { commandName } = interaction;

    if (commandName === 'santa') {
    
        const row = new MessageActionRow()
            .addComponents(
                new MessageButton()
                    .setCustomId('join')
                    .setLabel("Join Secret Santa!")
                    .setStyle('PRIMARY'),
            );

        await interaction.reply({content: `${interaction.user} has started a Secret Santa! Anybody who wants to join has 1 minute! Game Code: ${interaction.id}`, components: [row]});

        var fs = require('fs');

        var santaid = interaction.id;

        fs.readFile('./secretSantas.json', 'utf8', function readFileCallback(err, data){
            if (err){
                console.log(err);
            } else {
            try{
                obj = JSON.parse(data);
                obj.games.push(santaid);
                obj.users.push([]);
                obj.closed.push(false);
                json = JSON.stringify(obj); 
                fs.writeFile('./secretSantas.json', json, readFileCallback); 
            }
            catch(err){

            }
        }});

        await wait(60000);

        fs.readFile('./secretSantas.json', 'utf8', function readFileCallback(err, data){
            if (err){
                console.log(err);
            } else {
            try{
                obj = JSON.parse(data);
                index = obj.games.indexOf(santaid);
                obj.closed[index] = true;
                json = JSON.stringify(obj); 
                fs.writeFile('./secretSantas.json', json, readFileCallback); 
            }
            catch(err){

            }
        }});

        interaction.followUp("Registration for this Secret Santa is now closed!");

        fs.readFile('./secretSantas.json', 'utf8', function readFileCallback(err, data){
            if (err){
                console.log(err);
            } else {
            
                obj = JSON.parse(data);
                index = obj.games.indexOf(santaid);
                    
                var santas = []
                var receivers = []
                
                for(let i = 0; i < obj.users[index].length; i++){
                    santas.push(obj.users[index][i]);
                }

                function shuffle(array) {
                    let currentIndex = array.length,  randomIndex;
                  
                    // While there remain elements to shuffle...
                    while (currentIndex != 0) {
                  
                      // Pick a remaining element...
                      randomIndex = Math.floor(Math.random() * currentIndex);
                      currentIndex--;
                  
                      // And swap it with the current element.
                      [array[currentIndex], array[randomIndex]] = [
                        array[randomIndex], array[currentIndex]];
                    }
                  
                    return array;
                }

                shuffle(santas);

                for(let i = 1; i < obj.users[index].length; i++){
                    receivers.push(santas[i]);
                }
                receivers.push(santas[0]);


                for(let i = 0; i < santas.length; i++){
                    receive = client.users.cache.find(user => user.id === receivers[i])
                    client.users.cache.find(user => user.id === santas[i]).send(`You are the Secret Santa for ${receive.username}. Game Code: ${interaction.id}`);
                }
        }});

    }
    
});

client.on('interactionCreate', interaction => {

    if (!interaction.isButton()) return;

    var fs = require('fs');

    var santaid = interaction.message.interaction.id;

    fs.readFile('./secretSantas.json', 'utf8', function readFileCallback(err, data){
        if (err){
            console.log(err);
        } else {
        try{
            obj = JSON.parse(data);
            index = obj.games.indexOf(santaid);
            if(obj.closed[index]){
                interaction.reply({content: "This Secret Santa has already ended!", ephemeral: true});
                return;
            }
            if(obj.users[index].includes(interaction.user.id)){
                interaction.reply({content: "You are already in this Secret Santa!", ephemeral: true});
                return;
            }
            obj.users[index].push(interaction.user.id);
            interaction.reply({content: `${interaction.user} has joined the Secret Santa!`});
            json = JSON.stringify(obj); 
            fs.writeFile('./secretSantas.json', json, readFileCallback); 
        }
        catch(err){

        }
    }});

    

});

client.login(token);