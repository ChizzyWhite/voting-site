const Redis = require("ioredis");

const redisUrl = process.env.REDIS_URL || "redis://localhost:6379/0";
const redis = new Redis(redisUrl);

async function start() {
  console.log("VoteSphere worker started. Waiting for vote events...");

  while (true) {
    try {
      const result = await redis.brpop("vote_events", 0);
      const event = JSON.parse(result[1]);

      console.log(
        `[VOTE PROCESSED] Vote #${event.vote_id} -> ${event.candidate} | election ${event.election_id}`
      );
    } catch (error) {
      console.error("Worker error:", error.message);
      await new Promise(resolve => setTimeout(resolve, 2000));
    }
  }
}

start();
