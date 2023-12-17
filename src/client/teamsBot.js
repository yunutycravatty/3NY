const { TeamsActivityHandler, MessageFactory, CardFactory, TurnContext } = require("botbuilder");
const rawWelcomeCard = require("./adaptiveCards/welcome.json");
const rawLearnCard = require("./adaptiveCards/learn.json");
const cardTools = require("@microsoft/adaptivecards-tools");
const { MicrosoftAppCredentials } = require('botframework-connector');
const { geneFileName, getFileSize, writeFile } = require('./services/fileService');
const axios = require('axios');
const fs = require('fs');
const path = require('path');
const FILES_DIR = './Files';

class TeamsBot extends TeamsActivityHandler {
  constructor() {
    super();

    // record the likeCount
    this.likeCountObj = { likeCount: 0 };

    this.onMessage(async (context, next) => {
      console.log("Running with Response Activity.");

      TurnContext.removeRecipientMention(context.activity);

      const attachments = context.activity.attachments;
      const imageRegex = /image\/.*/;

      if (attachments && attachments[0] && attachments[0].contentType === 'application/vnd.microsoft.teams.file.download.info') {
        console.log("User provided file. Save locally.");
        const file = attachments[0];
        const config = {
            responseType: 'stream'
        };
        const filePath = path.join(FILES_DIR, file.name);
        await writeFile(file.content.downloadUrl, config, filePath);
        const reply = MessageFactory.text(`<b>${ file.name }</b> received and saved.`);
        reply.textFormat = 'xml';
        await context.sendActivity(reply);

      } else if (attachments && attachments[0] && imageRegex.test(attachments[0].contentType)) {
        console.log("User provided inline file. Save locally.");
        await this.processInlineImage(context);
        /* console.log("User provided inline file. Save locally.");
        const file = attachments[0];
        const config = {
            responseType: 'stream'
        };
        const filePath = path.join(FILES_DIR, file.contentUrl);
        await writeFile(file.contentUrl, config, filePath);
        const reply = MessageFactory.text(`<b>${ file.contentUrl }</b> received and saved.`);
        reply.textFormat = 'xml';
        await context.sendActivity(reply); */
      }
      else {
        console.log("User wrote message. Send to backend.");
        // Extract necessary data from the incoming message
        let txt = context.activity.text;
        
        const removedMentionText = TurnContext.removeRecipientMention(context.activity);
        if (removedMentionText) {
          // Remove the line break
          txt = removedMentionText.toLowerCase().replace(/\n|\r/g, "").trim();
        }
        
        let message = {
          "message": txt
        };
        // Send POST request to Flask server
        try {
          const response = await axios.post('http://127.0.0.1:5000/api/gpt-request', message);
          //let header = response.headers['content-type'];
          // Check if a file was sent in the response
          console.log(response)
          if (response.data.contentType === 'application/pdf') {
            // Get pdf from body
            const file = response.data.file;

            let fileName = file.name //response.headers['content-disposition'].split('filename=')[1];

            console.log(`File ${fileName} received and saved.`);
            // Process the file and save it locally
            
            const config = {
              responseType: 'stream'
            };

            // Save the file locally
            const filePath = path.join(FILES_DIR, fileName);
            console.log("filepaths: ", filePath)
            console.log("downloadUrl: ", file.downloadUrl)

            await writeFile(file.downloadUrl, config, filePath);
            
            

            const stats = fs.statSync(filePath);
            const fileSize = stats.size;

            // Send the file to the user
            await this.sendFileCard(context, file.name, fileSize);
          }
          else {
            // Send the response to the user
            // Normal case for conversation
            console.log(`Response: ${response.data} received.`);
            await context.sendActivity(response.data.answer);
          }

        } catch (error) {
          console.error(error);
        }
    }
      await next();
    });


  //   this.onMessage(async (context, next) => {
  //     TurnContext.removeRecipientMention(context.activity);
  //     const attachments = context.activity.attachments;
  //     const imageRegex = /image\/.*/;
  //     if (attachments && attachments[0] && attachments[0].contentType === 'application/vnd.microsoft.teams.file.download.info') {
  //         const file = attachments[0];
  //         const config = {
  //             responseType: 'stream'
  //         };
  //         const filePath = path.join(FILES_DIR, file.name);
  //         await writeFile(file.content.downloadUrl, config, filePath);
  //         const reply = MessageFactory.text(`<b>${ file.name }</b> received and saved.`);
  //         reply.textFormat = 'xml';
  //         await context.sendActivity(reply);
  //     } else if (attachments && attachments[0] && imageRegex.test(attachments[0].contentType)) {
  //         await this.processInlineImage(context);
  //     } else {
  //         const filename = 'teams-logo.png';
  //         const stats = fs.statSync(path.join(FILES_DIR, filename));
  //         const fileSize = stats.size;
  //         await this.sendFileCard(context, filename, fileSize);
  //     }
  //     await next();
  // });

    /* this.onMessage(async (context, next) => {
      const replyMessage = MessageFactory.text('');
      let returnCard;

      // Extract necessary data from the incoming message
      const message = context.activity;
      
      // Check if the user is sending the bot a file.
      if (message.attachments && message.attachments.length > 0) {
        const attachment = message.attachments[0];

        if (attachment.contentType === 'application/json') { // Adjust content type as needed
          const downloadInfo = attachment.content;
          if (downloadInfo) {
            returnCard = this.createFileInfoAttachment(downloadInfo, attachment.name, attachment.contentUrl);
            replyMessage.attachments = [returnCard];
          }
        }
      } else {
        // Illustrate creating a file consent card.
        returnCard = this.createFileConsentAttachment();
        replyMessage.attachments = [returnCard];
      }

      await context.sendActivity(replyMessage);

      // Continue with the processing of the next middleware
      await next();
    }); */


    
      // ...

    //   const removedMentionText = TurnContext.removeRecipientMention(context.activity);
    //   if (removedMentionText) {
    //     // Remove the line break
    //     txt = removedMentionText.toLowerCase().replace(/\n|\r/g, "").trim();
    //   }

    //   // Trigger command by IM text
    //   switch (txt) {
    //     case "welcome": {
    //       const card = cardTools.AdaptiveCards.declareWithoutData(rawWelcomeCard).render();
    //       await context.sendActivity({ attachments: [CardFactory.adaptiveCard(card)] });
    //       break;
    //     }
    //     case "learn": {
    //       this.likeCountObj.likeCount = 0;
    //       const card = cardTools.AdaptiveCards.declare(rawLearnCard).render(this.likeCountObj);
    //       await context.sendActivity({ attachments: [CardFactory.adaptiveCard(card)] });
    //       break;
    //     }
    //     /**
    //      * case "yourCommand": {
    //      *   await context.sendActivity(`Add your response here!`);
    //      *   break;
    //      * }
    //      */
    //   }

    //   // By calling next() you ensure that the next BotHandler is run.
    //   await next();
    // });

    // Listen to MembersAdded event, view https://docs.microsoft.com/en-us/microsoftteams/platform/resources/bot-v3/bots-notifications for more events
    this.onMembersAdded(async (context, next) => {
      const membersAdded = context.activity.membersAdded;
      for (let cnt = 0; cnt < membersAdded.length; cnt++) {
        if (membersAdded[cnt].id) {
          const card = cardTools.AdaptiveCards.declareWithoutData(rawWelcomeCard).render();
          await context.sendActivity({ attachments: [CardFactory.adaptiveCard(card)] });
          break;
        }
      }
      await next();
    });
  }

  /* createFileInfoAttachment(downloadInfo, name, contentUrl) {
    const card = new FileInfoCard({
      fileType: downloadInfo.fileType,
      uniqueId: downloadInfo.uniqueId,
    });

    const att = card.toAttachment();
    att.contentUrl = contentUrl;
    att.name = name;

    return att;
  }

  createFileConsentAttachment() {
    const acceptContext = {};
    // Fill in any additional context to be sent back when the user accepts the file.

    const declineContext = {};
    // Fill in any additional context to be sent back when the user declines the file.

    const card = new FileConsentCard({
      acceptContext,
      declineContext,
      sizeInBytes: 102635,
      description: 'File description',
    });

    const att = card.toAttachment();
    att.name = 'Example file';

    return att;
  } */

  // Invoked when an action is taken on an Adaptive Card. The Adaptive Card sends an event to the Bot and this
  // method handles that event.
  async onAdaptiveCardInvoke(context, invokeValue) {
    // The verb "userlike" is sent from the Adaptive Card defined in adaptiveCards/learn.json
    if (invokeValue.action.verb === "userlike") {
      this.likeCountObj.likeCount++;
      const card = cardTools.AdaptiveCards.declare(rawLearnCard).render(this.likeCountObj);
      await context.updateActivity({
        type: "message",
        id: context.activity.replyToId,
        attachments: [CardFactory.adaptiveCard(card)],
      });
      return { statusCode: 200 };
    }
  }

  async sendFileCard(context, filename, filesize) {
    const consentContext = { filename: filename };

    const fileCard = {
        description: 'This is the file I want to send you',
        sizeInBytes: filesize,
        acceptContext: consentContext,
        declineContext: consentContext
    };
    const asAttachment = {
        content: fileCard,
        contentType: 'application/vnd.microsoft.teams.card.file.consent',
        name: filename
    };
    await context.sendActivity({ attachments: [asAttachment] });
  }

  async handleTeamsFileConsentAccept(context, fileConsentCardResponse) {
      try {
          const fname = path.join(FILES_DIR, fileConsentCardResponse.context.filename);
          const fileInfo = fs.statSync(fname);
          const fileContent = Buffer.from(fs.readFileSync(fname, 'binary'), 'binary');
          await axios.put(
              fileConsentCardResponse.uploadInfo.uploadUrl,
              fileContent, {
                  headers: {
                      'Content-Type': 'image/png',
                      'Content-Length': fileInfo.size,
                      'Content-Range': `bytes 0-${ fileInfo.size - 1 }/${ fileInfo.size }`
                  }
              });
          await this.fileUploadCompleted(context, fileConsentCardResponse);
      } catch (e) {
          await this.fileUploadFailed(context, e.message);
      }
  }

  async handleTeamsFileConsentDecline(context, fileConsentCardResponse) {
      const reply = MessageFactory.text(`Declined. We won't upload file <b>${ fileConsentCardResponse.context.filename }</b>.`);
      reply.textFormat = 'xml';
      await context.sendActivity(reply);
  }

  async fileUploadCompleted(context, fileConsentCardResponse) {
      const downloadCard = {
          uniqueId: fileConsentCardResponse.uploadInfo.uniqueId,
          fileType: fileConsentCardResponse.uploadInfo.fileType
      };
      const asAttachment = {
          content: downloadCard,
          contentType: 'application/vnd.microsoft.teams.card.file.info',
          name: fileConsentCardResponse.uploadInfo.name,
          contentUrl: fileConsentCardResponse.uploadInfo.contentUrl
      };
      const reply = MessageFactory.text(`<b>File uploaded.</b> Your file <b>${ fileConsentCardResponse.uploadInfo.name }</b> is ready to download`);
      reply.textFormat = 'xml';
      reply.attachments = [asAttachment];
      await context.sendActivity(reply);
  }

  async fileUploadFailed(context, error) {
      const reply = MessageFactory.text(`<b>File upload failed.</b> Error: <pre>${ error }</pre>`);
      reply.textFormat = 'xml';
      await context.sendActivity(reply);
  }

  async processInlineImage(context) {
      const file = context.activity.attachments[0];
      const credentials = new MicrosoftAppCredentials(process.env.MicrosoftAppId, process.env.MicrosoftAppPassword);
      const botToken = await credentials.getToken();
      const config = {
          headers: { Authorization: `Bearer ${ botToken }` },
          responseType: 'stream'
      };
      const fileName = await geneFileName(FILES_DIR);
      const filePath = path.join(FILES_DIR, fileName);
      await writeFile(file.contentUrl, config, filePath);
      const fileSize = await getFileSize(filePath);
      const reply = MessageFactory.text(`Image <b>${ fileName }</b> of size <b>${ fileSize }</b> bytes received and saved.`);
      const inlineAttachment = this.getInlineAttachment(fileName);
      reply.attachments = [inlineAttachment];
      await context.sendActivity(reply);
  }

  getInlineAttachment(fileName) {
      const imageData = fs.readFileSync(path.join(FILES_DIR, fileName));
      const base64Image = Buffer.from(imageData).toString('base64');
      return {
          name: fileName,
          contentType: 'image/png',
          contentUrl: `data:image/png;base64,${ base64Image }`
      };
  }

}

module.exports.TeamsBot = TeamsBot;
