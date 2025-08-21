const mongoose = require('mongoose');
const { Kafka } = require('kafkajs');
const Tournament = mongoose.model('Tournament');

const kafka = new Kafka({
  clientId: 'api-producer',
  brokers: ['kafka:9092'] 
});
const producer = kafka.producer();

module.exports = function(app, Tournament) {
  app.post('/mi-endpoint', async (req, res) => {
    try {
      const tournaments = await Tournament.insertMany(req.body);

      // Enviar a Kafka cada torneo insertado
      await producer.connect();
      for (const tournament of tournaments) {
        await producer.send({
          topic: 'tournaments',
          messages: [
            { value: JSON.stringify(tournament) }
          ]
        });
      }
      await producer.disconnect();

      res.status(201).json({ message: `Torneos Insertados: ${tournaments.length}`, tournaments });
    } catch (error) {
      res.status(500).json({ error: error.message });
    }
  });
};