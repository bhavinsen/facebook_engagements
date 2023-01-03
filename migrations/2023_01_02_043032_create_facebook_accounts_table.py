from orator.migrations import Migration


class CreateFacebookAccountsTable(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create('facebook_accounts') as table:
            table.increments('id')
            table.integer('account_id')
            table.string('account_name')
            table.boolean('is_active')
            table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop('facebook_accounts')
