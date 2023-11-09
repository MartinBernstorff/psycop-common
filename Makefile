pr:
	make merge-main
	inv qpr

merge-main:
	git fetch
	git merge --no-edit origin/main

stash:
	# Git stash save creates a stash, even if there are no changes to stash. Needed for apply-latest-stash to work after a grow.
	git stash save

apply-latest-stash:
	git stash pop

enable-automerge:
	gh pr merge --auto --delete-branch

create-random-branch:
	@git checkout -b "$$(date +'%y_%m_%d_%H')_$(shell cat /dev/urandom | env LC_ALL=C tr -dc 'a-z' | fold -w 5 | head -n 1)"

grow:
	git pull
	make stash
	@echo "––– Growing into a new branch 🌳 –––"
	make create-random-branch
	make merge-main
	make apply-latest-stash

#################
# Short aliases #
#################
mm:
	make merge-main

g:
	make grow

gpr:
	make pr
	make g