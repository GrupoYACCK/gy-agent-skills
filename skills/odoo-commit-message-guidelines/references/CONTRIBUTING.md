---
title: OCA Guidelines (2018/08/24)
---

# Git

## Commit message

Write a **short** commit summary without prefixing it. It should not be
longer than 50 characters: This is a commit message

Then, in the message itself, specify the part of the code impacted by
your changes (module name, lib, transversal object, ...) and a
description of the changes. This part should be multiple lines no longer
than 80 characters.

- Commit messages are in English
- Merge proposals should follow the same rules as the title of the
  proposal is the first line of the merge commit and the description
  corresponds to commit description.
- Always put meaningful commit messages: commit messages should be self
  explanatory (long enough) including the name of the module that has
  been changed and the reason behind that change. Do not use single
  words like "bugfix" or "improvements".
- Avoid commits which simultaneously impact lots of modules. Try to
  split into different commits where impacted modules are different.
  This is helpful if we need to revert changes on a module separately.
- Only make a single commit per logical change set. Do not add commits
  such as "Fix pep8", "Code review" or "Add unittest" if they fix
  commits which are being proposed
- Use present imperative (Fix formatting, Remove unused field) avoid
  appending 's' to verbs: Fixes, Removes
- Use tags as [listed in the Odoo
  Guidelines](https://www.odoo.com/documentation/16.0/contributing/development/git_guidelines.html#tag-and-module-name)
  with the following extensions:
  - **[MIG]** for migrating a module

``` 
[FIX] website: remove unused alert div

Fix look of input-group-btn
Bootstrap's CSS depends on the input-group-btn element being the first/last
child of its parent.
This was not the case because of the invisible and useless alert.
```

``` 
[IMP] web: add module system to the web client

This commit introduces a new module system for the javascript code.
Instead of using global ...
```

When you open a PR, please check if the commit message is cut with
ellipsis. For example:

``` 
[FIX] module_foo: and this is my very long m[...]
```

When this happens, it means your message is too long. You should shorten
it. Start by rephrasing and keeping the summary very synthetic. The
explanation or motivation should be kept in the description of the
commit.

## Review

Peer review is the only way to ensure good quality of the code and to be
able to rely on the other developers. The peer review in this project
will be managed through Pull Requests. It will serve the following main
purposes:

- Having a second look on a code snippet to avoid unintended problems /
  bugs
- Avoid technical or business design flaws
- Allow the coordination and convergence of the developers by informing
  the community of what has been done
- Allow the responsibles to look at every devs and keep the interested
  people informed of what has been done
- Prevent addon incompatibilities when/if possible
- The rationale for peer review has its equivalent in Linus's law,
  often phrased: "Given enough eyeballs, all bugs are shallow"

Meaning "If there are enough reviewers, all problems are easy to
solve". Eric S. Raymond has written influentially about peer review in
software development:
<http://en.wikipedia.org/wiki/Software_peer_review>.

### Please respect a few basic rules:

- Read and follow the rules stated for the [module maturity
  levels](https://odoo-community.org/page/development-status).
- At least one of the review above must be from a member of the PSC or
  having write access on the repository (here one of the [OCA Core
  Maintainers](https://github.com/orgs/OCA/teams/core-maintainers). can
  do the job. You can notify them on Github using
  `@OCA/core-maintainers`)
- If you are in a hurry just send a mail at
  <contributors@odoo-community.org> or ask by chat in either of:
  - [OCA discord server](https://discord.gg/rN5xRdE)
  - [Matrix space #oca:matrix.org](https://matrix.to/#/#oca:matrix.org)
    (bridged to discord).
- Is the module generic enough to be part of community addons?
- Is the module duplicating features with other community addons?
- Does the documentation allow to understand what it does and how to use
  it?
- Is the problem it tries to resolve adressed the good way, using good
  concepts?
- Are there some use cases?
- Is there any setup in code? Should not!
- Are there demo data?
- Are the commit messages short, clear and clean?

Further reading:

- <https://insidecoding.wordpress.com/2013/01/07/code-review-guidelines/>

### There are the following important parts in a review:

- Start by thanking the contributor / developer for their work. No
  matter the issue of the PR, someone has done work for you, so be
  thankful for that.
- Be cordial and polite. Nothing is obvious in a PR.
- The description of the changes should be clear enough for you to
  understand their purpose and, if applicable, contain a demo in order
  to allow people to run and test the code
- Choose the review tag (comment, approve, rejected, needs
  information, ...) and don't forget to add a type of review to let
  people know:
  - Code review: means you look at the code
  - Test: means you tested it functionally speaking

While making the merge, please respect the author using the
`--author` option when committing. The author is found
using the git log command. Use the commit message provided by the
contributor if any.

### It makes sense to be picky in the following cases:

- The origin/reason for the patch/dev is not documented very well
- No adapted / convenient description written in the
  `__manifest__.py` file for the module
- Tests or scenario are not all green and/or not adapted
- Having tests is very much encouraged
- Issues with license, copyright, authorship
- Respect of Odoo/community conventions
- Code design and best practices

The long description try to explain the **why** not the **what**, the
**what** can be seen in the diff.

Pull requests can be closed if:

- there is no activity for 6 months

## Sources

This documentation was obtained from:

- https://github.com/OCA/odoo-community.org/blob/master/website/Contribution/CONTRIBUTING.rst#git
