# Quick Start

## requirements

The JumpScale portal requires two dependencies :
 - The JumpScale framework to be installed: [install JumpScale](../GettingStarted/Install.md) .
 - A connection to a running Mongodb instance : 
   - install on the current node  through :  
`j.tools.cuisine.local.apps.mongo.build()`

   - connect to running instance on the different node while installing through : `j.toolls.cuisine.apps.portal.install(mongodbip="<machine with mongo ip>", mongoport="<mongo port>")`

## To install your own portal with all local dependencies installed

Install base portal package locally:

```
j.tools.cuisine.local.portal.install()
```


Your portal code can now be placed @ `$basedir/apps/portal/main`

