This is a bare bones bot that connects to the Slack API and generates outputs based on @mention commands in Slack. As of now, the bot will output a message to a channel (hardcoded) upon connection, it will recognize the keyword 'do' and repeat whatever text follows 3 times (ie, input: @Ryan_Bot do a dance, output: a dance a dance a dance), it will ignore any Slack event that does not directly mention it, and it will output a goodbye message when it is disconnected (ie, 'See ya later!')  More features will be added soon.