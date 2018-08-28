# 查询用户甲(user_name)关注的用户的博客文章
select * from posts where author_id in (
	select followed_id from follows where follower_id = (
		select user_id from users where user_name='wanghuan'
	)
)