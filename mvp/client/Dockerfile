# Use Node.js LTS version as the base image
FROM node:latest

# Set the working directory inside the container
WORKDIR /app

# Copy package.json and package-lock.json to the working directory
COPY package.json package-lock.json ./

# Install dependencies
RUN npm install

# Copy the rest of the app files to the working directory
COPY . .

# Build the SvelteKit app
RUN npm run build

# Expose the port on which your Svelte app runs (change it according to your SvelteKit configuration if necessary)
EXPOSE 4173

# Set the command to start the SvelteKit app (adjust the start command as per your setup)
CMD ["npm", "run", "preview --host"]

# TODO replace this, find out how to actually serve the production build