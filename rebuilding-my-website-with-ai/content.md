---
title: "I Rebuilt My Entire Website in One Conversation with AI"
slug: rebuilding-my-website-with-ai
excerpt: "What happens when you let an AI pair-programmer handle everything — from tearing down your old cloud setup to publishing the blog post you're reading right now."
category: engineering
categoryName: Engineering
author: Alin Voinea
authorBio: Software Engineer
publishedAt: 2026-03-14T12:00:00Z
coverImage:
---

A few days ago, I sat down to rebuild my personal website. I had no plan, no timeline, no Jira board. Just a terminal, a cup of coffee, and GitHub Copilot CLI as my co-pilot.

What happened next surprised me. What was supposed to be a "quick cleanup" turned into a complete rebuild — and we did the whole thing without me ever leaving the conversation.

## My Website Had a Problem

Like a lot of developers, I'd over-engineered my personal blog. It had a separate CMS, its own database, multiple cloud services, and a monthly bill that felt silly for something that gets maybe a handful of visitors a day.

I was paying for 11 storage buckets, two content delivery networks, DNS hosting, an API gateway, and a bunch of other things I'd set up once and forgotten about. Classic cloud sprawl.

It was time to simplify.

## "Hey Copilot, What Am I Paying For?"

That's basically how it started. I asked Copilot to look at my AWS account and tell me what was costing money. Within minutes, it had a full inventory — every service, every resource, every forgotten log bucket (one had *106,000 files* in it).

Then I said something reckless: *"Clean it all up."*

And it did. Methodically. It knew you can't just delete a content delivery network — you have to disable it first and wait. It knew you have to empty storage buckets before deleting them. It knew DNS zones need their records removed first. Step by step, it cleaned out everything, and my AWS bill dropped to zero.

## The Moment It Corrected Me

Here's a small detail I keep thinking about. Early on, I told Copilot my domain was registered on AWS. It checked, and politely corrected me — the domain was actually on GoDaddy, just with some settings pointing to AWS.

That's the moment I realized this wasn't just a code generator. It was verifying things. It was being careful. That set the tone for everything that followed.

## Rethinking the Architecture

With the old setup gone, it was time to decide what comes next. I already had a partially built site running on Azure — a modern frontend, a Kotlin backend, and a full CMS system. But the CMS felt like too much. It needed its own server, its own database, a bunch of secret keys, and it didn't handle traffic spikes well.

For a personal blog? Overkill.

So I asked: *"Can we replace this with something simpler?"*

We landed on an idea that felt almost too simple: just write articles as plain text files and store them in the cloud. No database for content. No CMS admin panel. Just markdown files with a bit of metadata at the top, sitting in Azure's cloud storage.

The backend would read those files, convert the markdown to formatted HTML, and serve it to the frontend through the same interface as before. The frontend wouldn't even notice the change.

## The Big Rewrite

This is where things got impressive. Replacing the CMS wasn't a small change — it touched almost every part of the project. The backend needed new code to read from cloud storage and parse markdown. The infrastructure templates needed updating. The deployment pipeline had to drop the CMS entirely. Configuration files, environment variables, documentation — all of it needed to change.

**100 files changed. 19,000 lines of code deleted.** The project got dramatically simpler.

And here's the part that blew my mind: Copilot didn't just do this sequentially. It delegated work to specialized sub-agents — one focused on the backend code while another handled infrastructure — and ran them in parallel. It felt less like using a tool and more like managing a small team.

All tests passed after the migration. Coverage stayed above 90%.

## The Money Part

With the simpler architecture in place, we went through the remaining cloud costs line by line:

- Removed the dedicated database server — **saved about €25/month**
- Removed the CMS container — **saved about €15/month**
- Turned on "scale to zero" for the remaining services — **saved another €30/month**

**Total monthly cost went from roughly €80 to under €15.** The site only runs (and costs money) when someone actually visits it. For a personal blog, that's perfect. The only trade-off is a brief loading delay for the very first visitor after an idle period.

## What Surprised Me Most

**It wasn't about code generation.** I expected an autocomplete on steroids. What I got was a collaborator that understood the full picture — every file in the project, every cloud resource, every DNS record — and could work across all of them in a coherent way.

**The conversation *was* the project management.** No tickets, no planning docs. I described what I wanted in plain English, made decisions when asked, and watched it happen. When something broke, it diagnosed the problem and found a workaround.

**It checked its work.** The best moments weren't the flashy code rewrites — they were the quiet verification steps. Checking DNS propagation before configuring a domain. Running tests after every change. Correcting my wrong assumption about where my domain was registered.

**Simple is better.** The final setup is something I can maintain forever without thinking about it. Plain text files for content, a lightweight embedded database for the contact form, and two small services that sleep when nobody's visiting. That's it.

## What's Running Today

| What | How |
|------|-----|
| Frontend | React with modern tooling |
| Backend | Kotlin on Spring Boot |
| Blog content | Markdown files in cloud storage |
| Database | Lightweight embedded DB (contact form only) |
| Hosting | Azure with auto-scaling to zero |
| Deployment | Automatic via GitHub |
| Monthly cost | ~€12 |

And this article you're reading? It's one of those markdown files, sitting in cloud storage, served through the very pipeline we built together in that conversation.

---

*This entire project — from "what am I paying for?" to the blog post you're reading now — happened in a single conversation with an AI pair-programmer. The future of building software is weirder and more fun than I expected.*
