# See <https://www.ruby-forum.com/t/forcing-stdout-sync-for-scripts/48876/8>

alice_tuplespace: ruby -e '$stdout.sync = true; load($0 = ARGV.shift)' tuplespace.rb -c aliceTS.yaml
alice_adapter: ruby -e '$stdout.sync = true; load($0 = ARGV.shift)' adapter.rb -c aliceTS.yaml
bob_tuplespace: ruby -e '$stdout.sync = true; load($0 = ARGV.shift)' tuplespace.rb -c bobTS.yaml
bob_adapter: ruby -e '$stdout.sync = true; load($0 = ARGV.shift)' adapter.rb -c bobTS.yaml
chuck_tuplespace: ruby -e '$stdout.sync = true; load($0 = ARGV.shift)' tuplespace.rb -c chuckTS.yaml
chuck_adapter: ruby -e '$stdout.sync = true; load($0 = ARGV.shift)' adapter.rb -c chuckTS.yaml
