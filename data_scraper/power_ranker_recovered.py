f r o m   y a h o o _ o a u t h   i m p o r t   O A u t h 1 
 i m p o r t   x m l t o d i c t 
 i m p o r t   p a n d a s   a s   p d 
 i m p o r t   t i m e 
 o a u t h   =   O A u t h 1 ( N o n e ,   N o n e ,   f r o m _ f i l e = ' y a h o o _ o a u t h 1 . j s o n ' ) 
 u r l   =   ' h t t p : / / f a n t a s y s p o r t s . y a h o o a p i s . c o m / f a n t a s y / v 2 / l e a g u e / 3 6 4 . l . 8 0 9 1 / t r a n s a c t i o n s ' 
 r e s p o n s e   =   o a u t h . s e s s i o n . g e t ( u r l ) 
 
 d a t a   =   x m l t o d i c t . p a r s e ( r e s p o n s e . t e x t ) 
 
 t r a n s a c t i o n s   =   d a t a [ ' f a n t a s y _ c o n t e n t ' ] [ ' l e a g u e ' ] [ ' t r a n s a c t i o n s ' ] [ ' t r a n s a c t i o n ' ] 
 
 c o l u m n s   =   [ ' t i m e s t a m p ' , ' t e a m ' , ' t y p e ' , ' l a s t _ n a m e ' , ' f i r s t _ n a m e ' , ' p o s i t i o n ' , ' t e a m ' ] 
 r o w s _ l i s t   =   [ ] 
 f o r   t r a n s   i n   t r a n s a c t i o n s : 
         i f   ( t r a n s [ ' s t a t u s ' ]   = =   ' s u c c e s s f u l ' )   &   ( t r a n s [ ' t y p e ' ]   i n   { ' a d d / d r o p ' } ) : 
                 f o r   p l a y e r _ t r a n s   i n   t r a n s [ ' p l a y e r s ' ] [ ' p l a y e r ' ] : 
                           d   =   { } 
                           d [ ' l a s t _ n a m e ' ]   =   p l a y e r _ t r a n s [ ' n a m e ' ] [ ' l a s t ' ] 
                           d [ ' f i r s t _ n a m e ' ]   =   p l a y e r _ t r a n s [ ' n a m e ' ] [ ' f i r s t ' ] 
                           d [ ' p o s i t i o n ' ]   =   p l a y e r _ t r a n s [ ' d i s p l a y _ p o s i t i o n ' ] 
                           d [ ' t y p e ' ]   =   p l a y e r _ t r a n s [ ' t r a n s a c t i o n _ d a t a ' ] [ ' t y p e ' ] 
                           i f   d [ ' t y p e ' ]   = =   ' a d d ' : 
                                   d [ ' t e a m ' ]   =   p l a y e r _ t r a n s [ ' t r a n s a c t i o n _ d a t a ' ] [ ' d e s t i n a t i o n _ t e a m _ n a m e ' ] 
                                   d [ ' t e a m _ k e y ' ]   =   p l a y e r _ t r a n s [ ' t r a n s a c t i o n _ d a t a ' ] [ ' d e s t i n a t i o n _ t e a m _ k e y ' ] 
                           e l i f   d [ ' t y p e ' ]   = =   ' d r o p ' : 
                                   d [ ' t e a m ' ]   =   p l a y e r _ t r a n s [ ' t r a n s a c t i o n _ d a t a ' ] [ ' s o u r c e _ t e a m _ n a m e ' ] 
                                   d [ ' t e a m _ k e y ' ]   =   p l a y e r _ t r a n s [ ' t r a n s a c t i o n _ d a t a ' ] [ ' s o u r c e _ t e a m _ k e y ' ] 
                           d [ ' t i m e s t a m p ' ]   =   t i m e . s t r f t i m e ( " % a ,   % d   % b   % Y   % H : % M : % S " , t i m e . l o c a l t i m e ( f l o a t ( t r a n s [ ' t i m e s t a m p ' ] ) ) ) 
                           d [ ' d a t e ' ]   =   t i m e . s t r f t i m e ( " % Y - % m - % d " , t i m e . l o c a l t i m e ( f l o a t ( t r a n s [ ' t i m e s t a m p ' ] ) ) ) 
                           r o w s _ l i s t . a p p e n d ( d ) 
         e l i f   ( t r a n s [ ' s t a t u s ' ]   = =   ' s u c c e s s f u l ' )   &   ( t r a n s [ ' t y p e ' ]   i n   { ' a d d ' , ' d r o p ' } ) : 
                 d   =   { } 
                 d [ ' l a s t _ n a m e ' ]   =   t r a n s [ ' p l a y e r s ' ] [ ' p l a y e r ' ] [ ' n a m e ' ] [ ' l a s t ' ] 
                 d [ ' f i r s t _ n a m e ' ]   =   t r a n s [ ' p l a y e r s ' ] [ ' p l a y e r ' ] [ ' n a m e ' ] [ ' f i r s t ' ] 
                 d [ ' p o s i t i o n ' ]   =   t r a n s [ ' p l a y e r s ' ] [ ' p l a y e r ' ] [ ' d i s p l a y _ p o s i t i o n ' ] 
                 d [ ' t y p e ' ]   =   t r a n s [ ' p l a y e r s ' ] [ ' p l a y e r ' ] [ ' t r a n s a c t i o n _ d a t a ' ] [ ' t y p e ' ] 
                 i f   d [ ' t y p e ' ]   = =   ' a d d ' : 
                         d [ ' t e a m ' ]   =   t r a n s [ ' p l a y e r s ' ] [ ' p l a y e r ' ] [ ' t r a n s a c t i o n _ d a t a ' ] [ ' d e s t i n a t i o n _ t e a m _ n a m e ' ] 
                         d [ ' t e a m _ k e y ' ]   =   t r a n s [ ' p l a y e r s ' ] [ ' p l a y e r ' ] [ ' t r a n s a c t i o n _ d a t a ' ] [ ' d e s t i n a t i o n _ t e a m _ k e y ' ] 
                 e l i f   d [ ' t y p e ' ]   = =   ' d r o p ' : 
                         d [ ' t e a m ' ]   =   t r a n s [ ' p l a y e r s ' ] [ ' p l a y e r ' ] [ ' t r a n s a c t i o n _ d a t a ' ] [ ' s o u r c e _ t e a m _ n a m e ' ] 
                         d [ ' t e a m _ k e y ' ]   =   t r a n s [ ' p l a y e r s ' ] [ ' p l a y e r ' ] [ ' t r a n s a c t i o n _ d a t a ' ] [ ' s o u r c e _ t e a m _ k e y ' ] 
                 d [ ' t i m e s t a m p ' ]   =   t i m e . s t r f t i m e ( " % a ,   % d   % b   % Y   % H : % M : % S " , t i m e . l o c a l t i m e ( f l o a t ( t r a n s [ ' t i m e s t a m p ' ] ) ) ) 
                 d [ ' d a t e ' ]   =   t i m e . s t r f t i m e ( " % Y - % m - % d " , t i m e . l o c a l t i m e ( f l o a t ( t r a n s [ ' t i m e s t a m p ' ] ) ) ) 
                 r o w s _ l i s t . a p p e n d ( d ) 
 
 d f   =   p d . D a t a F r a m e ( r o w s _ l i s t ) 
 d f . t o _ c s v ( ' . / t r a n s a c t i o n s / t r a n s a c t i o n s . c s v ' , i n d e x = F a l s e , s e p = ' , ' ,   e n c o d i n g = ' u t f - 8 ' ) 